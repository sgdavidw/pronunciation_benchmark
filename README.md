# pronunciation_benchmark

Suppose you read or memorize the English speech manuscript to make a speech and record the speech with the Zoom meeting. In that case, you may want to compare the manuscript with the Zoom meeting audio transcript to learn which words/sentences the Zoom meeting transcript can recognize accurately from your speech.

If you save the English speech manuscript as a text file ref_speech.org, and download the Zoom meeting recording audio transcript and save it as hyp_speech.vtt. You can run the following script:  
`python3 compare ref_speech.org hyp_speech.vtt`

# Prerequisite:

You need to install a Python module asr-evaluation to evaluate ASR hypotheses (i.e. word error rate and word recognition rate) on your system.
The easiest way to install asr-evaluation is using pip:  
`pip install asr-evaluation`
For more details about asr-evaluation, please see https://github.com/belambert/asr-evaluation

# Output
