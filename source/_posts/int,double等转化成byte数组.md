title: 'int,double等转化成byte数组'
tags:
  - byte数组
  - java
  - 转换
id: 913
categories:
  - Java
date: 2014-09-24 22:23:09
---

最近需要用到这个功能，本来想自己写，怕写错了，上网找了一下，都没找到合适的。看了solr与源码中的TrieField.java,有这一部分的代码，copy到这里。
``` java
public class ByteUtil {
    public static int toInt(byte[] arr) {
        return (arr[0] << 24) | ((arr[1] & 0xff) << 16)
                | ((arr[2] & 0xff) << 8) | (arr[3] & 0xff);
    }

    public static long toLong(byte[] arr) {
        int high = (arr[0] << 24) | ((arr[1] & 0xff) << 16)
                | ((arr[2] & 0xff) << 8) | (arr[3] & 0xff);
        int low = (arr[4] << 24) | ((arr[5] & 0xff) << 16)
                | ((arr[6] & 0xff) << 8) | (arr[7] & 0xff);
        return (((long) high) << 32) | (low & 0x0ffffffffL);
    }

    public static float toFloat(byte[] arr) {
        return Float.intBitsToFloat(toInt(arr));
    }

    public static double toDouble(byte[] arr) {
        return Double.longBitsToDouble(toLong(arr));
    }

    public static byte[] toArr(int val) {
        byte[] arr = new byte[4];
        arr[0] = (byte) (val >>> 24);
        arr[1] = (byte) (val >>> 16);
        arr[2] = (byte) (val >>> 8);
        arr[3] = (byte) (val);
        return arr;
    }

    public static byte[] toArr(long val) {
        byte[] arr = new byte[8];
        arr[0] = (byte) (val >>> 56);
        arr[1] = (byte) (val >>> 48);
        arr[2] = (byte) (val >>> 40);
        arr[3] = (byte) (val >>> 32);
        arr[4] = (byte) (val >>> 24);
        arr[5] = (byte) (val >>> 16);
        arr[6] = (byte) (val >>> 8);
        arr[7] = (byte) (val);
        return arr;
    }

    public static byte[] toArr(float val) {
        return toArr(Float.floatToRawIntBits(val));
    }

    public static byte[] toArr(double val) {
        return toArr(Double.doubleToRawLongBits(val));
    }
}
```