#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import multiprocessing

class myProcess(multiprocessing.Process):
   def __init__(self, lock, queue, L):
      self.lock = lock
      self.queue = queue
      self.L = L
      multiprocessing.Process.__init__(self)
   def run(self):
      while True:
         self.lock.acquire()
         try:
            data = queue.get_nowait()
            self.L.append(data)
            self.queue.task_done()
         except Queue.Empty:
            return
         finally:
            self.lock.release()

lock = multiprocessing.Lock()
queue = multiprocessing.JoinableQueue(-1)
manager = multiprocessing.Manager()
L = manager.list()

for word in 'Split this sentence in words.'.split():
   queue.put_nowait(word)

processes = [myProcess(lock, queue, L) for i in range(2)]
for process in processes:
   process.start()

queue.join()
print L

