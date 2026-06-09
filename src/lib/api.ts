export const API_BASE_URL = '';

export function base64ToBlob(base64: string, mimeType: string = 'image/jpeg'): Blob {
  let raw = base64;
  if (base64.includes(',')) raw = base64.split(',')[1];
  const byteCharacters = atob(raw);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: mimeType });
}

export async function fetchHistogramData(imageBlob: Blob): Promise<number[]> {
  const formData = new FormData();
  formData.append('file', imageBlob, 'image.jpg');
  
  const response = await fetch(`${API_BASE_URL}/api/histogram`, {
    method: 'POST',
    body: formData,
    headers: {
      'ngrok-skip-browser-warning': 'true',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch histogram');
  }

  const data = await response.json();
  if (data.histogram) {
    return data.histogram;
  }
  throw new Error('Invalid histogram data returned');
}

export async function processImage(
  endpoint: string,
  imageBlob: Blob,
  params: Record<string, string | number> = {}
): Promise<Blob> {
  const formData = new FormData();
  formData.append('file', imageBlob, 'image.jpg');
  
  for (const [key, value] of Object.entries(params)) {
    formData.append(key, String(value));
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    body: formData,
    headers: {
      'ngrok-skip-browser-warning': 'true',
    },
  });

  if (!response.ok) {
    let errorDetail = 'Image processing failed';
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errorDetail;
    } catch (e) {
      // fallback
    }
    throw new Error(errorDetail);
  }

  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    const data = await response.json();
    if (data.image) {
      return base64ToBlob(data.image, 'image/jpeg');
    } else if (data.result_image) {
      return base64ToBlob(data.result_image, 'image/jpeg');
    }
    throw new Error('API returned JSON without an image');
  } else {
    // Binary blob
    return await response.blob();
  }
}
