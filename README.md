# cat-shape-prediction

### Cat shape classification (loaf, standing up, sitting down) using transfter learning with VGG16. 
   ### Final model results: val_loss: 0.2863 - val_accuracy: 0.9468.

Steps:
* Get data - I used Reddit API and Pushshift API to fetch images of the desired cat shapes I wished to predict. 
  * Each image was converted to "RGB" size (224, 224).
  * (The subreddits in questions are CatLoaf, CatsSittingDown and CatsStandingUp)
* Process Data - remove duplicates script was used and also manual processing.
  * Sample images for each category can be seen as zip on 'images' folder.
* Model the data using VGG16 transfer learning.
   * The model is too large to upload to github. Here's the learning curve:

![Prediction pyplot](https://github.com/MayaBenj/cat-shape-prediction/blob/main/pyplot.jpg)
