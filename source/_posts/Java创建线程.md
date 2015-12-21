title: Java创建线程
date: 2015-12-21 20:44:03
tags: 线程
categories: Java
---
在Java中创建线程有两中方法，一种是实现Runnable接口，一种是继承Thread类
## 实现Runnable接口
1. 将任务代码迁移到实现Runnable接口的类的run方法中
```
class MyRunnable implements Runnable {
    public void run() {
        task code
    }
}
```
2. 创建一个类对象:
Runnable r = new MyRunnable()
3. 由Runnable创建一个Thread对象
Thread t = new Thread(r)
4. 启动线程
t.start()
完整例子如下:
```
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Child: " + Thread.currentThread().getId());
        
    }
    public static void main(String[] arg) {
        for (int i = 0; i < 5; i++) {
            Runnable r = new MyRunnable();
            Thread t = new Thread(r);
            t.start();
        }
        System.out.println("Parent: " + Thread.currentThread().getId());
    }
}
```
输出结果如下：
Child: 8
Child: 9
Child: 10
Child: 11
Parent: 1
Child: 12
这里不能直接调用run方法，因为这样不会创建新的线程:
```
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Child: " + Thread.currentThread().getId());
    }
    public static void main(String[] arg) {
        for (int i = 0; i < 5; i++) {
            Runnable r = new MyRunnable();
//          Thread t = new Thread(r);
//          t.start();
            r.run();
        }
        System.out.println("Parent: " + Thread.currentThread().getId());
    }
}
```
输出结果如下：
Child: 1
Child: 1
Child: 1
Child: 1
Child: 1
Parent: 1
可以看到id都是一样的,也就是这里没有创建新的线程.
## 继承Thread类
```
class MyThread extends Thread {
    public void run() {
        task code
    }
} 
```
完整例子如下:
```
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Child: " + Thread.currentThread().getId()); 
    }
    public static void main(String[] arg) {
        for (int i = 0; i < 5; i++) {
            Thread t = new MyThread();
            t.start();
        }
        System.out.println("Parent: " + Thread.currentThread().getId());
    }
}
```
输出结果如下：
Child: 8
Child: 9
Child: 10
Child: 11
Parent: 1
Child: 12
这里不能直接调用t.run()，因为这样不会创建新的线程
```
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Child: " + Thread.currentThread().getId()); 
    }
    public static void main(String[] arg) {
        for (int i = 0; i < 5; i++) {
            Thread t = new MyThread();
//          t.start();
            t.run();
        }
        System.out.println("Parent: " + Thread.currentThread().getId());
    }
}
```
结果如下：
Child: 1
Child: 1
Child: 1
Child: 1
Child: 1
Parent: 1
可以看到id都是一样的。
查看Thread类的源码就会发现问题的所在.
```
public synchronized void start() {
        /**
         * This method is not invoked for the main method thread or "system"
         * group threads created/set up by the VM. Any new functionality added
         * to this method in the future may have to also be added to the VM.
         *
         * A zero status value corresponds to state "NEW".
         */
        if (threadStatus != 0)
            throw new IllegalThreadStateException();

        /* Notify the group that this thread is about to be started
         * so that it can be added to the group's list of threads
         * and the group's unstarted count can be decremented. */
        group.add(this);

        boolean started = false;
        try {
            start0();
            started = true;
        } finally {
            try {
                if (!started) {
                    group.threadStartFailed(this);
                }
            } catch (Throwable ignore) {
                /* do nothing. If start0 threw a Throwable then
                  it will be passed up the call stack */
            }
        }
    }

    private native void start0();
```
在start方法中调用native方法start0()，虽然看不到它的具体实现，但可以推测这里创建了新的线程，然后调用run方法。而run方法中，则没有创建线程相关的代码
```
public void run() {
    if (target != null) {
        target.run();
    }
}
```
关于两种方法的区别，可以看[http://stackoverflow.com/questions/541487/implements-runnable-vs-extends-thread](http://stackoverflow.com/questions/541487/implements-runnable-vs-extends-thread), 推荐使用实现Runnable接口的方法。
