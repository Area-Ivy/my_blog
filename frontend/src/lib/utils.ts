export function cn(...args: Array<string | false | null | undefined>) {
  return args.filter(Boolean).join(' ');
}

// Centralized API base URL, configured via Vite env
export const API_BASE: string = (import.meta as any).env.VITE_API_BASE_URL as string;