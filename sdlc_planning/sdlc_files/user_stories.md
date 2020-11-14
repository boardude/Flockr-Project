# **Product:** Flockr #

## **Epic 1:** Grouping channels ##
### **User story 1.1** ###
As a user of Flockr who uses multiple channels for a similar purpose, I want to be able to group those channels together so that my channels list appears more organised.
### *Task 1.1* ###
Create new grouping system for channels acting as folders to files.
### *UAC 1.1 - rule-based* ###
* Can create channel groups
* Can delete channel groups
* Can move existing channels inside channel groups
* Can move existing channels out of channel groups
* Can create new channels inside channel groups

### **User story 1.2** ###
As a user of channel groups, I want to name the groups myself so that I can better organise channels by naming their categories (ex: Work, School, Friends, etc.).
### *Task 1.2* ###
Add ability for channel group names to be user-defined.
### *UAC 1.2 - rule-based* ###
* Channel groups have default names
* Creator of the channel group can change its name from default to a custom string

</br>

## **Epic 2:** Advanced messaging features ##
### **User story 2.1** ###
As a user of Flockr, I want the ability to send direct messages so that I can privately message another user instead of putting the message in channels.
### *Task 2.1* ###
Add the ability to send other users direct messages independent of channels.
### *UAC 2.1 - rule-based* ### 
* User can select the option to send a direct message
* User can choose which user to start a direct message conversation with
* User can send messages directly to the other user in the direct message chat without using channels
* New participants cannot be invited to or join an existing direct message chat

### **User story 2.2** ###
As a user of Flockr, I want to be able to see the status of a message after it has been sent so that I know when the other user(s) have received and/or seen it.
### *Task 2.2* ##
Add the ability to see the status of a message after it has been sent. Four statuses specifically: failed to send, sent, delivered/received, seen.
### *UAC 2.2 - scenario-based* ###
* **Scenario:** Showing status of a message after it has been sent  
* **Given:** The user is in a channel or direct message  
* **When:** User sends a message channel or direct messages  
* **Then:** Flockr detects and displays the current status of the message (failed to send, sent, delivered, seen).

### **User story 2.3** ###
As a user of Flockr, I want to be able to remove a message after it has been sent into a channel or direct message in the case when I sent something to the wrong person, the message contained a mistake, or when I simply have changed my mind.
### *Task 2.3* ###
Add the option for sent messages in channels and direct messages to be removed by the original sender.
### *UAC 2.3 - scenario-based* ###
* **Scenario:** Remove a sent message  
* **Given:** The user sends a message in a channel or direct message  
* **When:** The users selects the "remove" option for the message  
* **Then:** Flockr backend removes the message from the database  
* **And:** Flockr frontend removes the messages from the channel and stops it from being displayed to other users.

### **User story 2.4** ###
As a user of Flockr, I want to be able to edit a message after it has been sent into a channel or direct message so that I can correct a message instead or removing it and sending a new one.
### *Task 2.4* ###
Add the option for sent messages in channels and direct messages to be edited by the original sender.
### *UAC 2.4 - scenario-based* ###
* **Scenario:** Edit a sent message  
* **Given:** The user sends a message in a channel or direct message  
* **When:** The users selects the "edit" option for the message  
* **Then:** Flockr displays a text box where the user can edit the original message  
* **When:** User selects "Finish"  
* **Then:** Flockr modifies the message in the backend to reflect the user's edits   
* **And:** Flockr frontend displays the user's modified message in the original message's place  
* **Or when:** User selects "Cancel"  
* **Then:** Flockr backend discards all of the user's edits  
* **And:** Flockr frontend continues to display the original message.

</br>

## **Epic 3:** File sharing in channels and direct messages ##
### **User story 3.1** ###
As a user of Flockr, I want to be able to share files in channels and direct messages so I can collaborate better with my team and eliminate the need to email files to other users.
### *Task 3.1* ### 
Add the ability for users to send and receive files in channels and direct messages.
### *UAC 3.1 - rule-based* ###
* Users can send local files into a channel or direct message
* Any user that is a part of the channel or direct message can download and retrieve sent files
* All file types are supported

### **User story 3.2** ###
As a user of Flockr, I want to be able to see and download files I have shared in the past as part of the message history so I don't have to keep resending the same files.
### *Task 3.2* ###
Add some form of *longer*-term file persistence/storage to Flockr.
### *UAC 3.2 - rule-based* ###
* Any file that are shared in a channel or direct message remains available for any user to retrieve/download for a period of longer than 30 days
* Past shared files appear in reverse chronological order as part of the message history as if it were a message

</br>

## **Epic 4:** Real-time audiovisual communication ##
### **User story 4.1** ###
As a user of Flockr, I want to be able to host video calls in Flockr to replace conventional collaboration methods such as face-to-face meetings.
### *Task 4.1* ###
Add ability to have real-time video calls between multiple users in channels or between two users in direct messages.
### *UAC 4.1 - rule-based* ###
* Can make real-time video calls in direct messages (between two users) and in channels (between two or more users)
* Video calls are able to stream camera (video) and microphone (voice) inputs
* Hosts can end the video call at any time
* Any participant can leave a video call at any time
* If the host leaves the video call the video call is ended

### **User story 4.2** ###
As a user of Flockr, I want to be able to have audio-only calls for quick and informal meetings where there is no need to appear in front of a camera.
### *Task 4.2* ###
Add option to turn off/on the camera in video calls.
### *UAC 4.2 - rule-based* ###
* Users can turn off and on their camera stream at any time during a video call 
* Users can continue to participate in the call voice-only after turning off their camera

### **User story 4.3** ###
As a participant of a video call, I want to be able to mute my mic at any time during the call in case if a family member is talking to me and I don't want other participants of the call to hear my conversation.
### *Task 4.3* ###
Add the option to turn off/on the microphone in video calls
### *UAC 4.3* ###
* Users can turn off and on their microphone input at any time during a video call
* Users can hold a dedicated key to temporarily unmute their microphone when it is in a muted (off) state

### **User story 4.4** ###
As a user of Flockr, I want to be able to mute my mic and turn off my camera before joining a meeting to avoid causing any disruption.
### *Task 4.4* ###
Add panel to check and set audio and video settings after clicking on 'join call' button, but prior to actually joining the call.
### *UAC 4.4 - scenario based* ###
* **Scenario:** Set up video call settings before joining a video call
* **Given:** The user is in a channel or direct message
* **When:** The user has selected to start or join a video call
* **Then:** Flockr displays a screen where users can set video and audio settings for the voice call, including the option to join with the camera off and mic muted
* **When:** The user selects and confirms settings
* **Then:** Flockr connects the user to the video call

### **User story 4.5** ###
As the host of a video call in Flockr, I want to have the option to record the calls as video or audio files so that any non-participants have access to information shared during the meeting.
### *Task 4.5* ###
Add the option to record video calls as video or audio files, but only to the host of each meeting or a Flockr owner.
### UAC 4.5 - scenario-based ###
* **Scenario:** Host records a video call as a video or audio file
* **Given:** A video call has been started and the user is the host of the call (started the call or has been given host status)
* **When:** The user (host) selects the option to record the call
* **And:** Chooses whether to record as a video file or voice-only as an audio file
* **Then:** Flockr begins to record the video call
* **When:** The host ends the recording or the video call itself
* **Then:** Flockr saves the recording as a file on the user's local machine

### **User story 4.6** ###
As a participant of a video call, I want the option to share my screen to other participants so that they can all see the same thing I am referring to, just like in a face-to-face meeting.
### *Task 4.6* ###
Add the option for screen-sharing by any participant during a video call.
### *UAC 4.6 - scenario-based* ###
* **Scenario:** Screen-sharing during video calls
* **Given:** The user is a participant of the video call and no other participant is sharing their screen
* **When:** The user selects the option to screen-share
* **Then:** Flockr asks whether to share the entire screen or an application window only.
* **When:** The user makes a selection
* **Then:** Flockr displays the user's screen or an application window (depending on selection) as the main video object of the call.
* **When:** The user selects the option to stop sharing his/her screen
* **Then:** Flockr stops displaying the user's screen as the main video object

### **User story 4.7** ###
As the host of a video call, I want to be able to manage participants so that I can mute or remove any participant, to combat any trolling behaviour that often plagues the world of online conferencing.
### *Task 4.7* ###
Give the host of video calls the ability to mute or remove any participant.
### *UAC 4.7 - rule-based* ###
* The host of a video call can remove any participant at any time during the video call
* The host can mute the audio input of any participant
* The host can unmute the audio input of any participant

### **User story 4.8** ###
As the host of a video call, I want to be able to transfer host privileges to any participant, in the case where I have started the video call but is not supposed to act as the host of the meeting.
### *Task 4.8* ###
Add the ability for the host of video calls to transfer host status to any other participant. 
### *UAC 4.8 - rule-based* ###
* The host of a video call can transfer host status to any other participant in the video call
* After host status is transferred to the other user, host status is removed from the current user
* There is only one host in each video call
* Any participant can request host status from the host. The host can either accept or reject the request
