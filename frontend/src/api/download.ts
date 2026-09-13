import { api } from "./client";

export async function descargarExcel(url: string, filename: string): Promise<void> {
  const res = await api.get(url, { responseType: "blob" });
  const blobUrl = window.URL.createObjectURL(res.data as Blob);
  const a = document.createElement("a");
  a.href = blobUrl;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(blobUrl);
}
