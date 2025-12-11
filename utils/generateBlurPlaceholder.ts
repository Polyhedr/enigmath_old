import type { ImageProps } from "./types";

// Frontend-safe blur placeholder generator
export default async function getBase64ImageUrl(image: ImageProps) {
  // Simple static base64 blur (light gray gradient)
  // You could also generate a tiny blurred canvas if you prefer.
  return (
    "data:image/png;base64," +
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFgwJ/l0Nv8wAAAABJRU5ErkJggg=="
  );
}
