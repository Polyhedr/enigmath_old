// utils/cachedImages.ts
import fs from "fs";
import path from "path";
import type { ImageProps } from "./types";

let cachedResults: ImageProps[] | null = null;

export default async function getResults(): Promise<ImageProps[]> {
  if (cachedResults) return cachedResults;

  const enigmasDir = path.join(process.cwd(), "public", "enigmas");
  if (!fs.existsSync(enigmasDir)) return [];

  const folderNames = fs.readdirSync(enigmasDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);

  cachedResults = folderNames.map((folder, idx) => {
    const folderPath = path.join(enigmasDir, folder);

    // IMAGE DETECTION
    const imageFile = fs.readdirSync(folderPath).find((f) =>
      /\.(jpe?g|png|webp|gif|avif)$/i.test(f)
    );

    if (!imageFile) {
      console.warn(`No image found in folder "${folder}"`);
    }

    // ---------------------------
    // LOAD tags.txt
    // ---------------------------
    const tagsFile = path.join(folderPath, "tags.txt");
    let tags: string[] = [];

    if (fs.existsSync(tagsFile)) {
      try {
        const raw = fs.readFileSync(tagsFile, "utf8");

        tags = raw
          .split(/[\n,]/) // split newline OR comma
          .map((t) => t.trim())
          .filter((t) => t.length > 0);
      } catch (err) {
        console.error(`Cannot read tags.txt in "${folder}"`, err);
      }
    }

    return {
      id: idx + 1,
      folderName: folder,
      src: imageFile ? `/enigmas/${encodeURIComponent(folder)}/${encodeURIComponent(imageFile)}` : "",
      width: 720,
      height: 480,
      computer,
      difficulty,
      tags,
    };
  });

  return cachedResults;
}
