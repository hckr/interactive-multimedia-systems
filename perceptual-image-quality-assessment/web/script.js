const imageEl = document.querySelector("#image");

const imageVariants = imageVariantsGenerator("../image-grayscale.png", [
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
]);

document.querySelectorAll("#rankButtons button").forEach((button) => {
  button.onclick = async () => {
    const {value, done} = await imageVariants.next();
    if (done) {
      image.src = '';
      return;
    }
    image.src = value;
  };
});

async function* imageVariantsGenerator(origImageSrc, qualityVariants) {
  const dataUrls = shuffle(
    await prepareImageVariantsAsDataURLs(origImageSrc, qualityVariants)
  );
  for (const dataUrl of dataUrls) {
    yield dataUrl;
  }
}

function prepareImageVariantsAsDataURLs(origImageSrc, qualityVariants) {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  return new Promise((resolve, reject) => {
    const origImage = new Image();
    origImage.onload = () => {
      canvas.width = origImage.width;
      canvas.height = origImage.height;
      ctx.drawImage(origImage, 0, 0);

      resolve(
        qualityVariants.map((quality) =>
          canvas.toDataURL("image/jpeg", quality)
        )
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
