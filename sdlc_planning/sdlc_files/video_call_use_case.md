# **Use case - Real-time video calls (Epic 4)** #

**Use case:** Host and record a video call in a Flockr channel

**Goal in context:** For Flockr to more effectively replace face-to-face collaboration, users need to be able to have real-time multi-user video conferences. 

**Scope:** Flockr backend & frontend

**Level:** Primary Task

**Preconditions:** User needs to be registered and logged into Flockr. User needs to be part of a channel.

**Success end condition:** User is back in the channel after hosting video call with other users, exchanging information via real-time video, and then ending the video call after the meeting. A recording 

**Failed end conditions (any of the following):** 
* User is unable to host a video call continuously.
* User is unable to exchange the planned amount of information via real-time video due to a Flock error.
* User is unable to end the video call upon clicking the 'End call' button.
* A one-to-one recording is not saved to the user's local machine after either the recording or video call is ended.

**Primary actor:** The user, who is to host the video call.

**Trigger:** The user clicks on "Start video call".

## **Steps taken** ##
*MAIN SUCCESS SCENARIO*  
* **Step 1.** Flockr shows a 'Call settings' screen for user to confirm audio and video settings.  
* **Step 2.** User confirms settings selection, leaving both microphone and camera enabled.  
* **Step 3.** Flockr starts the video call for the user and shows a prompt in the channel that a video call is in progress.  
* **Step 4.** Other users in the channel join the video call via the prompt.  
* **Step 5.** As with the first user, Flockr asks each joining user to confirm their call settings before actually joining the call.  
* **Step 6.** Once all intended participants have joined, user selects "Start recording".  
* **Step 7.** Flockr asks user whether to record the call as a video or audio file.  
* **Step 8.** User selects record as a video.  
* **Step 9.** Flockr begins recording the video call in the background.  
* **Step 10.** User selects "Share screen".  
* **Step 11.** Flockr asks the user whether to share the entire screen or a single application window.
* **Step 12.** User selects option to share entire screen.
* **Step 13.** Flockr streams user's screen to the video call and makes it the primary video object
* **Step 14.** Flockr continues the video call without issue.
* **Step 15.** User clicks "End call" button.
* **Step 16.** Flockr ends the video call for every participant (given user is host), and returns to the channel interface.
* **Step 17.** Flockr saves a video recording of the call as a file on the user's local machine (as per user's request in steps 6-8).
