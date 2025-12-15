// utils/types.ts
export interface ImageProps {
  id: number;
  src: string;
  width: number;
  height: number;
  blurDataUrl?: string;
  folderName?: string;
  difficulty?: number;
  computer?: number; 
  title?: string;
  tags?: string[];
}

