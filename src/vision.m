clear
close all


%Use Pre-Recorded Video
v = aviReader('../data/sample1.avi');
videoFrame = readFrame(v);

%Use Webcam Streaming
%cam = webcam;
%videoFrame = snapshot(cam);

% Capture one frame to get its size.
frameSize = size(videoFrame);

% Create the video player object.
videoPlayer = vision.VideoPlayer('Position', [100 100 [frameSize(2), frameSize(1)]+30]);

runLoop = true;
numPts = 0;
frameCount = 0;

while runLoop && hasFrame(v)
    videoFrame = readFrame(v);
    %videoFrame = snapshot(cam);
    
    
    % Display the annotated video frame using the video player object.
    step(videoPlayer, videoFrame);

    % Check whether the video player window has been closed.
    runLoop = isOpen(videoPlayer);
end

% Clean up.
clear cam;
release(videoPlayer);
release(pointTracker);
release(faceDetector);