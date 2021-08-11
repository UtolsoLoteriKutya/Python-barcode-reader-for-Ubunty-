# Python barcode reader for Ubuntu.Banana Pi,PC
A simple barcode reader module for python on Ubuntu. It's made to call it from your program (instantiation needed to your main app), but it runs individually too for trying out the barcode reader.

Tested on Banana pi m3 and PC. 

Hopefully it works with most of USB 1D and 2D readers. (tested with 5-7 different ones) Feel free to use it, i hope it helps!:) I am interested in your feedbacks, so please drop a comment!

Update: I've found one 2D barcode scanner of which doesn't work with this driver: Symbol DS2208. For some reason, it builds up a different file/folder structure in the os, what is not compatible with my method. Certainly there is a way to handle it in this code, but it needs some extension.
