

let song;
let features;
let rmsValues = [];
let centroidValues = [];
let onsets = [];

function preload() {
  soundFormats('mp3', 'wav');
  song = loadSound('media/musicgen_out.wav');
  features = loadJSON('media/audio_features.json');
}

function setup() {
  createCanvas(800, 600);
  song.play();

  rmsValues = features.rms;
  centroidValues = features.centroid;
  onsets = features.onsets;
}

function draw() {
  background(0);

  if (!song.isPlaying()) {
    return;
  }

  let t = song.currentTime();
  let duration = song.duration();

  let frameIndex = int(map(t, 0, duration, 0, rmsValues.length));
  frameIndex = constrain(frameIndex, 0, rmsValues.length - 1);

  let rms = rmsValues[frameIndex];
  let centroid = centroidValues[frameIndex];

  let radius = rms * 1000; // Scale volume
  let hue = map(centroid, 0, 8000, 0, 255);

  colorMode(HSB, 255);
  fill(hue, 200, 255);
  noStroke();
  ellipse(width/2, height/2, radius, radius);
}