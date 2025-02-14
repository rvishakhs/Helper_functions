def get_lines(filename):
    '''
    This function reads the content of the file we are passing and returns the lines as a list

    Args:
        filename : a string containing the traget file path

    Returns:
        A list of strings per lines
    '''
    with open(filename, 'r') as reader:
        return reader.readlines()

def preprocess_text(filename):
    '''
    Returns a list of dictionaries of abstract line data
    Takes in filename, reads it's contents and sorts through each line,
    extracting things like the target label, the text of the sentence,
    how many sentences are in the current abstract and what sentence number the target line is

    Args:
      filename: a string of the target text file to read and extract line data
      from.

  Returns:
      A list of dictionaries each containing a line from an abstract,
      the lines label, the lines position in the abstract and the total number
      of lines in the abstract where the line is from. For example:

      [{"target": 'CONCLUSION',
        "text": The study couldn't have gone better, turns out people are kinder than you think",
        "line_number": 8,
        "total_lines": 8}]
    '''

    input_lines = get_lines(filename) # Get all lines from the file
    abstract_lines = " " # Create an empty abstract
    abstract_samples = [] # Create an empty list of abstracts

    # Loop through each line of the lines
    for line in input_lines:
        if line.startswith("###"): # Check if the line is an ID Line
            abstract_id = line  # Get the absract ID we can use this later if we wanted
            abstract_lines = "" # Again set the abstract line as empty
        elif line.isspace(): # Check to see if the line is a new line
            abstract_line_split = abstract_lines.splitlines() # Split the abstarct into seperate lines

            # Iterate through each line in abstarct and count them at the same time
            for abstract_line_no, abstract_line in enumerate(abstract_line_split):
                line_data = {} # Create an empty dict
                target_text_split = abstract_line.split('\t') # Split the target and text from each line
                line_data["target"] = target_text_split[0] # get target label
                line_data["text"] = target_text_split[1].lower() # get target text and lower it
                line_data["line_number"] = abstract_line_no # what number line does the line appear in the abstract?
                line_data["total_lines"] = len(abstract_line_split) - 1 # how many total lines are in the abstract? (start from 0)
                abstract_samples.append(line_data) # add line data to abstract samples list
        else: # if the above conditions aren't fulfilled, the line contains a labelled sentence
            abstract_lines += line
    return abstract_samples

def calculate_results(y_true, y_pred):
  """
  Calculates model accuracy, precision, recall and f1 score of a binary classification model.

  Args:
      y_true: true labels in the form of a 1D array
      y_pred: predicted labels in the form of a 1D array

  Returns a dictionary of accuracy, precision, recall, f1-score.
  """
  # Calculate model accuracy
  model_accuracy = accuracy_score(y_true, y_pred) * 100
  # Calculate model precision, recall and f1 score using "weighted average
  model_precision, model_recall, model_f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted")
  model_results = {"accuracy": model_accuracy,
                  "precision": model_precision,
                  "recall": model_recall,
                  "f1": model_f1}
  return model_results
