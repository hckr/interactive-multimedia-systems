"use strict";

const imageEl = document.querySelector("#image");
const descriptionEl = document.querySelector("#description");
const rankButtonsEl = document.querySelector("#rank-buttons");
const endScreenEl = document.querySelector("#end-screen");
const resultTextarea = document.querySelector("#result");

document.querySelector("#call-to-action").onclick = async () => {
  descriptionEl.classList.add("hidden");
  rankButtonsEl.classList.remove("hidden");
  showNextVariant();
};

const qualityVariants = [
  0.05,
  0.15,
  0.25,
  0.35,
  0.45,
  0.55,
  0.65,
  0.75,
  0.85,
  0.95,
];
const imageVariants = imageVariantsGenerator(
  "../image-grayscale.png",
  qualityVariants
);

const results = [];

async function showNextVariant() {
  const {
    value,
    done,
  } = await imageVariants.next();

  if (done) {
    showEndScreen();
    return;
  }

  const { quality, dataUrl } = value;

  imageEl.src = dataUrl;

  rankButtonsEl.querySelectorAll("button").forEach((button, key) => {
    button.onclick = () => {
      results.push([quality, key + 1]);
      showNextVariant();
    };
  });
}

function showEndScreen() {
  rankButtonsEl.classList.add("hidden");
  imageEl.classList.add("hidden");
  endScreenEl.classList.remove("hidden");
  resultTextarea.value = JSON.stringify(results);
}

resultTextarea.onclick = function() {
  this.select();
}

async function* imageVariantsGenerator(origImageSrc, qualityVariants) {
  const dataUrls = shuffle(
    await prepareImageVariants(origImageSrc, qualityVariants)
  );
  for (const dataUrl of dataUrls) {
    yield dataUrl;
  }
}

function prepareImageVariants(origImageSrc, qualityVariants) {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  return new Promise((resolve, reject) => {
    const origImage = new Image();
    origImage.onload = () => {
      canvas.width = origImage.width;
      canvas.height = origImage.height;
      ctx.drawImage(origImage, 0, 0);

      resolve(
        qualityVariants.map((quality) => ({
          quality,
          dataUrl: canvas.toDataURL("image/jpeg", quality),
        }))
      );
    };
    origImage.onerror = reject;
    origImage.src = origImageSrc;
  });
}

function shuffle(array) {
  return array
    .map((n) => [Math.random(), n])
    .sort()
    .map((n) => n[1]);
}
