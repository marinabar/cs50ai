First added one Conv2D layer, a Maxpool one with 4x4 grid, a flattening layer and 2 other hidden ones.
Then added a SGD optimizer plus a softmax activation at the end. 
The model did a pretty bad job, with a 0.056 accuracy after 10 epochs.
I tried adding two dropout layers, with a 0.5 parameter. It also did a horrible job.
Changing one of the parameters of the droput layers to 0.3 and the other to 0.8 didn't do much either. But after changing both of them to 0.3, the model became way more accurate.
After printing out the model summary I decided I wanted to try adding another Conv2D layer, so I did, along with a Maxpool with a 2x2 pool size.
It just made things worse, and the accuracy went from 0.9 to 0.7.
I then proceed to add another Dropout layer before the 2nd Conv2D layer.
Didn't change much things either, therefore I deleted the convolutional layers I had previously added. 
+ Put another Dense layer 
it really improved the model A LOT (92% accuracy!)
Tried adding another Dense layer + dropout, though deleted the dropout layer right after, and got again the 0.92 accuracy.

Increased the size of the first hidden layer, and decreased the pool size.
Achieved 95% accuracy! 

 




