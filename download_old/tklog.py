import tkinter as tk
from tkinter import Toplevel, PhotoImage
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename
import logging
import threading
import queue


__version = 'V0.12'


"""
About the sync argument for log interfaces (added in V0.12):
You should be VERY VERY careful to decide set sync=True, since it is very
often cause dead lock. Normally, it only should be set in background
thread which needs to log to GUI text windows.
You can not set sync=True in the event loop of GUI!!
"""

# When too many threads put info in the queue, and there is only one
# thread to get and consume, a lot of info maybe stocked in the queue,
# and it needs so much time to get and consume them all. So, set a length
# to the queue to slow down all the crazy threads.
# But, there is another risk. If your GUI event handler put info directly,
# without in a thread, your program might be deadlock if the queue is not
# long enough.
# So, to be a little balance in between, here we go:
QUEUE_LEN = 2048
# And, put method is set with block=False.

class TextboxHandler(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.insert("end", msg + "\n")


class tklog(ScrolledText):
    """readonly scrolled text log class"""

    def __init__(self, **kw):
        super().__init__(**kw, state=tk.DISABLED, cursor='plus',
                         wrap=tk.WORD, font=('monospace',12))
        self.tag_config('TITLE', foreground='blue')
        self.tag_config('INFO', foreground='black')
        self.tag_config('DEBUG', foreground='gray')
        self.tag_config('WARNING', foreground='hotpink')
        self.tag_config('ERROR', foreground='red')
        self.tag_config('CRITICAL', foreground='red', underline=1)
        self.rpop = tk.Menu(self, tearoff=0)
        self.rpop.add_command(label='Export', command=self._copyas)
        self.rpop.add_command(label='Copy', command=self._copyto)
        self.rpop.add_command(label='Clean', command=self.clean)
        self.autoscroll = tk.IntVar(value=1)
        self.rpop.add_checkbutton(label='Autoscrolling',
                                  command=None,
                                  variable=self.autoscroll)
        self.editable = tk.IntVar(value=0)
        self.rpop.add_checkbutton(label='Editable',
                                  command=self._editable,
                                  variable=self.editable)
        self.bind('<Button-3>', self._popup)
        self.bind('<Button-1>', self._popdown)
        self.bind('<Up>', self._lineUp)
        self.bind('<Down>', self._lineDown)
        self.pList = []
        self.q = queue.Queue(QUEUE_LEN)
        self.stop = 0
        self.wt = threading.Thread(target=self._writer,
                                   args=(), daemon=True)
        self.wt.start()

    def destroy(self):
        self.stop = 1
        self.q.put(None)  # q.get is blocked, so we need put sth.

    def _popup(self, event):
        self.rpop.post(event.x_root, event.y_root)

    def _popdown(self, event):
        self.rpop.unpost()
        self.focus_set()

    def _copyas(self):
        saveTo = asksaveasfilename()
        if not isinstance(saveTo, str): return
        if saveTo == '': return
        with open(saveTo, 'w') as f:
            f.write(self.get('1.0', tk.END))

    def _copyto(self):
        self.clipboard_clear()
        try:
            selection = self.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass  # skip TclError while no selection
        else: self.clipboard_append(selection)

    def _editable(self):
        if self.editable.get():
            self.config(state=tk.NORMAL)
        else:
            self.config(state=tk.DISABLED)

    def _chState(self, state):
        if self.editable.get():
            return
        if state == 'on':
            self.config(state=tk.NORMAL)
        if state == 'off':
            self.config(state=tk.DISABLED)

    def _writer(self):
        while True:
            info = self.q.get()
            if self.stop: break
            try:
                if isinstance(info, threading.Event):
                    info.set()
                    continue
                pos = info[:9].find('@')
                if pos == -1:
                    self._chState('on')
                    self.insert(tk.END, '[undefined format]: '+info)
                    self._chState('off')
                else:
                    if info[:pos] == 'CLEAN':
                        self._chState('on')
                        self.delete('1.0', tk.END)
                        self._chState('off')
                    elif info[:pos] == 'PNG' or info[:pos] == 'GIF':
                        try:
                            self.pList.append(PhotoImage(file=info[pos+1:]))
                            self._chState('on')
                            self.image_create(
                                tk.END,
                                image=self.pList[len(self.pList)-1])
                            self.insert(tk.END, '\n', 'DEBUG')
                            self._chState('off')
                        except Exception as e:
                            self._chState('on')
                            self.insert(tk.END, repr(e)+'\n', 'DEBUG')
                            self._chState('off')
                    else:
                        self._chState('on')
                        self.insert(tk.END, info[pos+1:], info[:pos])
                        self._chState('off')
                if self.autoscroll.get() == 1:
                    self.see(tk.END)
            except tk.TclError:
                break

    def _log(self, level, content, end, sync):
        self.q.put(level+'@'+content+end, block=False)
        if sync:
            self._syn_log()

    def _syn_log(self):
        wait2go = threading.Event()
        self.q.put(wait2go, block=False)
        wait2go.wait()

    def title(self, content, end='\n', *, sync=False):
        self._log('TITLE', content, end, sync)

    def info(self, content, end='\n', *, sync=False):
        self._log('INFO', content, end, sync)

    # directly call info will raise, why?
    log = info

    def debug(self, content, end='\n', *, sync=False):
        self._log('DEBUG', content, end, sync)

    def warning(self, content, end='\n', *, sync=False):
        self._log('WARNING', content, end, sync)

    def error(self, content, end='\n', *, sync=False):
        self._log('ERROR', content, end, sync)

    def critical(self, content, end='\n', *, sync=False):
        self._log('CRITICAL', content, end, sync)

    def png(self, pngFile, *, sync=False):
        self._log('PNG', pngFile, '', sync)

    def gif(self, gifFile, *, sync=False):
        self._log('GIF', gifFile, '', sync)

    def _lineUp(self, event):
        self.yview('scroll', -1, 'units')

    def _lineDown(self, event):
        self.yview('scroll', 1, 'units')

    def clean(self):
        self.q.put('CLEAN@', block=False)