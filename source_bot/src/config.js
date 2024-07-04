const fs = require('fs');
const mime = require('mime-types');
const path = require('path');

const path_attachment = 'audio_samples/';

[path_attachment].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir);
});

async function saveMediaToFile(buffer, mimetype, timestamp) {
  const extension = mime.extension(mimetype);
  const filename = `${timestamp}.${extension}`;
  const filepath = path.join(path_attachment, filename);

  await fs.promises.writeFile(filepath, buffer);
  console.log(`${filename} was saved in the directory ${path_attachment}`);
  return filename;
}

module.exports = {
  saveMediaToFile,
  path_attachment,
};
