// utils/types.ts
export interface ImageProps {
  id: number;
  src: string;
  width: number;
  height: number;
  blurDataUrl?: string;
  folderName?: string;
  tags?: string[];
}

