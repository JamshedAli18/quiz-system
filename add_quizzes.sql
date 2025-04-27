-- Insert the three quizzes into the quizzes tabl
INSERT INTO quizzes (title, time_limit) VALUES
('Generative AI', 600),
('Machine Learning', 600),
('Deep Learning', 600);

-- Get the quiz IDs (assuming the IDs are 1, 2, 3 for simplicity; adjust if there are existing quizzes)
-- Generative AI Quiz (quiz_id assumed as 1)
INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option) VALUES
(1, 'What is a key feature of Generative AI?', 'Classifying data', 'Predicting outcomes', 'Generating new data', 'Optimizing algorithms', 'C'),
(1, 'Which model is commonly used for text generation in Generative AI?', 'SVM', 'GAN', 'LSTM', 'K-Means', 'C'),
(1, 'What does GAN stand for?', 'Generalized Algorithm Network', 'Generative Adversarial Network', 'Global Attention Network', 'Gradient Accumulation Node', 'B'),
(1, 'In a GAN, what is the role of the Discriminator?', 'Generate new data', 'Evaluate generated data', 'Optimize the Generator', 'Store training data', 'B'),
(1, 'Which of these is a popular Generative AI application?', 'Image classification', 'Object detection', 'Text-to-image generation', 'Sentiment analysis', 'C'),
(1, 'What is a challenge in training GANs?', 'Overfitting', 'Mode collapse', 'Underfitting', 'High accuracy', 'B'),
(1, 'Which loss function is typically used in GANs?', 'Cross-Entropy Loss', 'Mean Squared Error', 'Adversarial Loss', 'Hinge Loss', 'C'),
(1, 'What is the purpose of the Generator in a GAN?', 'Evaluate real data', 'Generate fake data', 'Classify data', 'Reduce dimensionality', 'B'),
(1, 'Which of these is an example of a Generative AI model?', 'BERT', 'ResNet', 'VAE', 'YOLO', 'C'),
(1, 'What is a common dataset used for training Generative AI models?', 'MNIST', 'CIFAR-10', 'ImageNet', 'All of the above', 'D');

-- Machine Learning Quiz (quiz_id assumed as 2)
INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option) VALUES
(2, 'What is the primary goal of supervised learning?', 'Cluster data', 'Predict outcomes', 'Generate data', 'Reduce dimensions', 'B'),
(2, 'Which algorithm is used for classification tasks?', 'K-Means', 'Linear Regression', 'Decision Tree', 'PCA', 'C'),
(2, 'What does overfitting mean in Machine Learning?', 'Model performs well on training data but poorly on test data', 'Model performs poorly on both training and test data', 'Model performs well on test data only', 'Model cannot be trained', 'A'),
(2, 'Which metric is used to evaluate a classification model?', 'Mean Squared Error', 'Accuracy', 'R-Squared', 'Mean Absolute Error', 'B'),
(2, 'What is the purpose of a validation set?', 'Train the model', 'Test the model', 'Tune hyperparameters', 'Generate data', 'C'),
(2, 'Which technique helps prevent overfitting?', 'Increasing model complexity', 'Regularization', 'Adding more features', 'Reducing training data', 'B'),
(2, 'What is a common activation function in neural networks?', 'Sigmoid', 'Linear', 'Exponential', 'Quadratic', 'A'),
(2, 'Which algorithm is unsupervised?', 'Logistic Regression', 'K-Means Clustering', 'SVM', 'Random Forest', 'B'),
(2, 'What does SVM stand for?', 'Simple Vector Machine', 'Support Vector Machine', 'Standard Vector Model', 'Synthetic Variance Model', 'B'),
(2, 'What is the purpose of feature scaling?', 'Reduce training time', 'Improve model accuracy', 'Normalize data', 'All of the above', 'D');

-- Deep Learning Quiz (quiz_id assumed as 3)
INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option) VALUES
(3, 'What is a key component of a neural network?', 'Neuron', 'Cluster', 'Decision Tree', 'Feature Vector', 'A'),
(3, 'What does CNN stand for?', 'Convolutional Neural Network', 'Cascaded Neural Network', 'Compressed Neural Network', 'Centralized Neural Node', 'A'),
(3, 'Which layer is typically used in CNNs for feature extraction?', 'Dense Layer', 'Convolutional Layer', 'Pooling Layer', 'Dropout Layer', 'B'),
(3, 'What is the purpose of a pooling layer in a CNN?', 'Increase parameters', 'Reduce spatial dimensions', 'Add noise', 'Classify data', 'B'),
(3, 'Which optimization algorithm is commonly used in Deep Learning?', 'Gradient Descent', 'K-Means', 'Random Search', 'Greedy Algorithm', 'A'),
(3, 'What is a common problem in Deep Learning models?', 'Underfitting', 'Vanishing gradients', 'Overtraining', 'Low accuracy', 'B'),
(3, 'Which framework is popular for Deep Learning?', 'TensorFlow', 'Pandas', 'NumPy', 'Matplotlib', 'A'),
(3, 'What is the role of an activation function?', 'Normalize data', 'Introduce non-linearity', 'Reduce dimensions', 'Classify data', 'B'),
(3, 'Which type of neural network is used for sequential data?', 'CNN', 'RNN', 'MLP', 'GAN', 'B'),
(3, 'What is a dropout layer used for?', 'Increase model complexity', 'Prevent overfitting', 'Speed up training', 'Generate data', 'B');