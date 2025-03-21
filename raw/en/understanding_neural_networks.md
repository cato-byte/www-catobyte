## Understanding Neural Networks

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Image created by ChatGPT, OpenAI. 7th October 2024 ](../../images/understanding_neural_networks_title_img.webp)


Hey everyone! So today I want to review and give a basic introduction to neural networks so we can understand in very general terms the technology that makes AI models to function. I have another post about [NLP](../post/nlp_introduction.html) if you want to ggo deeper I think it can be useful as is other set of techniques that allow tools such as Gemini and ChatGPT understand what you are trying to say. 

A good introduction can be found on this  [mit article](https://news.mit.edu/2017/explained-neural-networks-deep-learning-0414) from which I took some insights for writing this post. I also recommend you that you read my other post [a simple introduction to machine learning](../a_simple_introduction_to_machine_learning.html) so you can have a basic foundation on machine learning.


### 1. What are Neural Networks?

A neural network is a computational model inspired by the structure of the human brain, consisting of layers of artificial neurons connected by "weights" that determine the strength of connections between them. These networks can learn from data and improve over time through a process called training. At its most basic form, a neural network has three types of layers: the input layer, which receives raw data (such as an image's pixel values or words in a sentence); hidden layers, which perform the actual computation and whose number and complexity determine the network's ability to learn deep, abstract features; and the output layer, which produces the result, such as predicting a label (e.g., "cat" or "dog" for an image classifier or the next word in a sentence for a language model).


### 2. Basic Components of a Neural Network

To understand how a neural network works, we need to break down its fundamental components. At the heart of the network are neurons (also called nodes), which are the basic computational units. Each neuron receives inputs, processes them by applying weights, and produces an output. The strength of the connections between neurons is determined by weights, which control how much influence one neuron's output has on the next neuron's input. Through the training process, weights learn the importance of different features. Another important element is the bias, which is a constant added to the weighted sum of inputs, giving the network flexibility to model complex relationships. Finally, after the inputs are summed and weighted, the neuron applies an activation function (such as ReLU or Sigmoid) to decide if it should "fire" (output a significant value) or remain inactive. Activation functions introduce non-linearity into the network, enabling it to solve complex problems that simple linear models cannot.


### 3. Training, Validation, and Retraining

Training a neural network involves feeding it data and adjusting its weights through a process called backpropagation. During training, the network is presented with a large dataset of input-output pairs, such as images and their corresponding labels. For each data point, the network makes a prediction, and the difference between the predicted and actual output (called the loss) is calculated. To minimize this loss, the network uses backpropagation and gradient descent. Backpropagation involves propagating the loss back through the network to update the weights, while gradient descent is an optimization algorithm that adjusts the weights to minimize the loss in the next iteration. Validation is crucial during training to monitor the network's performance on a separate dataset, ensuring it is not overfitting and can generalize well to new data. If the network's performance is lacking, retraining may be necessary. This can involve changing the network’s structure, adding more layers, or applying regularization techniques to improve generalization and prevent overfitting.

### 4. A real world example

Now let's view a simple real world example to ground these concepts. Let's try to predict wether an email is spam or not. n this example, we want our neural network to classify emails as spam or not spam. Each email is represented as a feature vector, where each feature could indicate: the presence of specific words ,the frequency of certain punctuation marks, the presence of certain keywords associated with spam (like “free,” “buy now,” etc.).  The process of transforming features such as words, punctuation marks, or other non-numeric data into numerical values for machine learning is commonly called feature extraction or feature engineering. Specifically, when dealing with text data, this process is often referred to as vectorization or text vectorization.

Let's review this process more in detail:


First, preprocessing the text involves cleaning the raw data. This step includes removing unnecessary elements such as stop words (like "the", "is", "in"), special characters, or numbers (unless they are essential). After cleaning the text, it’s often converted to lowercase to ensure uniformity, so words like “Spam” and “spam” are treated the same. For example, the sentence “Free money!!! Click now to claim your reward!!!” becomes “free money click now claim reward”.

The process of transforming features such as words, punctuation marks, or other non-numeric data into numerical values for machine learning is called feature extraction or feature engineering. Specifically, when working with text data, this transformation is often referred to as vectorization or text vectorization. This is essential for machine learning models, as they require numerical inputs to make predictions or classifications.

Let’s go through the steps of feature extraction and vectorization in the context of a spam classification task, where the goal is to classify whether an email is spam or not based on the presence of certain words, punctuation marks, and other relevant features.

First, preprocessing the text involves cleaning the raw data. This step includes removing unnecessary elements such as stop words (like "the", "is", "in"), special characters, or numbers (unless they are essential). After cleaning the text, it’s often converted to lowercase to ensure uniformity, so words like “Spam” and “spam” are treated the same. For example, the sentence “Free money!!! Click now to claim your reward!!!” becomes “free money click now claim reward”.

Next, we extract features from the cleaned text. Common features include word frequencies, punctuation frequencies, the presence of specific words (like "free" or "win" that are associated with spam), and the length of the message. These features can provide useful information for distinguishing between spam and non-spam emails.

Once the features are identified, the next step is vectorization, where the textual data is converted into a numerical format that a machine learning model can process. One common method is Bag of Words (BoW), where a vocabulary of all unique words in the training dataset is created. For each document (email), a vector is created based on the frequency of each word in this vocabulary. For example, if the vocabulary consists of words like "free", "money", "claim", and "reward", each email will be represented by a vector that counts how many times each word appears in that email.

Example:
For the sentences:

Email 1: "Free money, claim your reward now!"
Email 2: "Buy now, special offer on products!"
Vocabulary: ["free", "money", "claim", "your", "reward", "now", "buy", "special", "offer", "on", "products"]

Email 1 Vector: [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
Email 2 Vector: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

Each value in the vector represents the frequency of the corresponding word in the email.

Another technique for vectorization is Term Frequency-Inverse Document Frequency (TF-IDF), which adjusts word frequencies by accounting for how common or rare a word is across all documents. This method helps emphasize words that appear frequently in a particular document but are rare across the entire dataset, making them more useful for classification tasks.

In some cases, One-Hot Encoding is used, especially for categorical features. For example, if you are checking for the presence of certain words or punctuation marks, you can assign a binary value (1 for presence, 0 for absence). For example, if you’re checking for the words "money" and "free", an email containing both words might be represented by the vector \[1, 1\], while an email with neither would be represented as \[0, 0\].

Finally, after applying vectorization, all the features are combined into a final feature vector. This vector, which includes word frequencies, punctuation counts, and other features, serves as the input to a machine learning algorithm. For instance, an email’s feature vector might look like this: \[3 (free), 1 (money), 0 (offer), 2 (exclamation marks), 5 (length)\]. This feature vector is then used by a machine learning model, such as a neural network or decision tree, to classify the email as spam or not spam.

In summary, transforming non-numeric data like words and punctuation into numerical values is called vectorization or feature extraction. By applying methods like Bag of Words, TF-IDF, and One-Hot Encoding, we can convert text data into a format suitable for machine learning models. These methods help capture the essential patterns and features in the data that are important for tasks such as spam classification.


Next, we define our neural network’s architecture. In this example, the input layer will contain one neuron per feature extracted from the email (e.g., word frequencies or character counts). The input neurons connect to a hidden layer, where we specify the number of neurons based on the complexity of the problem—say, 64 neurons in one hidden layer. These neurons apply an activation function like ReLU to add non-linearity, enabling the network to learn complex relationships between features. The final output layer has two neurons, one for each class: "spam" and "not spam," which generate probabilities for each class. Using the softmax activation function ensures the outputs are probabilities that sum to 1, indicating the likelihood that an email belongs to each class.

During training, each email passes through the network in a process called forward propagation. The network calculates a weighted sum of the inputs at each neuron, applies activation functions, and outputs a prediction (probability of being spam or not). We then use a loss function, such as categorical cross-entropy, to measure the difference between the network's prediction and the true label of the email.

To improve accuracy, we apply backpropagation to adjust the weights based on the loss. In backpropagation, the loss is propagated backward through the network, calculating how much each weight contributed to the error. Using an optimization algorithm like gradient descent, the weights are adjusted to minimize the error. This process repeats over multiple epochs, where each epoch represents one pass through the entire training dataset.

Throughout training, we periodically validate the model's performance on a validation dataset to detect overfitting. If the model performs well on training data but poorly on validation data, we may need to adjust hyperparameters (e.g., learning rate, number of layers) or introduce regularization techniques to help generalize to new emails.

Finally, once training is complete and the model performs well on the validation dataset, we test it on the testing dataset to confirm it can accurately classify unseen emails. By following this workflow, the neural network learns from labeled examples, refines its understanding of what distinguishes spam from legitimate emails, and becomes a reliable classifier for detecting spam in real-world applications.


### 5. How Much Data Does a Neural Network Need?

The amount of data depends on the complexity of the problem. Simple tasks, like recognizing handwritten numbers, may require less data, while more complex tasks, such as image classification or natural language processing, need vast amounts of data to generalize well and avoid overfitting.

### 6. What are Weights, and How Are They Determined?

Weights represent the strength of connections between neurons, initially set randomly but fine-tuned during training. As the network learns, weights are adjusted to reduce the loss function’s value. Through this optimization process, the network becomes more accurate, improving its predictive abilities.

### 7. How Neural Networks Process Images vs. Text

While the core concepts of neural networks (weights, neurons, activation functions) are the same, the structure and design of networks for images versus text can differ significantly:

Neural Networks for Image Processing: These networks are often Convolutional Neural Networks (CNNs), which are designed to process grid-like data, like pixels in an image. CNNs use specialized layers called convolutional layers that apply filters to the image, capturing features like edges, textures, and patterns at different levels. This hierarchical approach helps CNNs learn to recognize complex objects by building up from simple patterns.

Neural Networks for Text Processing: Text-based neural networks often use Recurrent Neural Networks (RNNs) or Transformers. RNNs are designed to handle sequential data (like words in a sentence) and maintain an internal state that helps them "remember" previous inputs. This is crucial for understanding context in language. Modern models like Transformers (used in models like GPT-4) rely on attention mechanisms to understand the relationships between words without requiring them to be processed sequentially, allowing for more efficient and scalable language understanding.


### 8. Similarities Between Image and Text Networks

Despite these differences, neural networks for both images and text share several similarities:

Layered Architecture: Both image and text networks use multiple layers (input, hidden, and output) to extract features and make predictions.

Weights and Backpropagation: The process of adjusting weights via backpropagation and gradient descent applies to both types of networks.

Activation Functions: Non-linear activation functions (like ReLU) are used in both types of networks to introduce non-linearity, allowing the model to capture complex relationships.


### 9. Key Differences

Data Structure: Images are 2D (or 3D with color channels), so convolutional layers and pooling are used to process spatial relationships. Text, on the other hand, is sequential, so networks need mechanisms to capture the order of words and their dependencies.

Preprocessing: Image data often needs to be resized, normalized, or augmented (e.g., rotated or flipped) to help the network generalize. Text data requires tokenization (breaking sentences into words or characters) and may involve embedding the words into continuous vectors.


### Conclusion

Neural networks are powerful tools that enable AI to tackle complex problems across fields like computer vision and natural language processing. At the core of these networks are simple components—neurons, weights, and activation functions—but their real strength lies in their ability to learn and adapt through processes like training, backpropagation, and validation. Whether processing images or text, neural networks share the same foundational principles, but they adapt their architectures to the specific nature of the data they handle, making them versatile and effective across a wide range of applications.
