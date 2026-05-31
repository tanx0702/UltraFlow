import { getToken } from '@/utils/auth';

export function useUpload() {
  async function uploadFile(tempPath: string): Promise<string> {
    const baseURL = import.meta.env.VITE_API_BASE_URL;
    return new Promise((resolve, reject) => {
      uni.uploadFile({
        url: `${baseURL}/api/common/upload`,
        filePath: tempPath,
        name: 'file',
        header: { token: getToken() || '' },
        success: (res) => {
          if (res.statusCode === 200) {
            const body = JSON.parse(res.data);
            resolve(body.data);
          } else {
            reject(new Error('上传失败'));
          }
        },
        fail: () => reject(new Error('上传失败')),
      });
    });
  }

  return { uploadFile };
}
