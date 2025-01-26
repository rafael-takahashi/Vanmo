import { api } from '@/lib/axios'

interface getUserPictureHeader {
  token: string | undefined
}

export async function getUserPicture({ token }: getUserPictureHeader) {
    try {
        const response = await api.get('/usuario/buscar_foto_perfil', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        return response.data;
    } catch (error: any) {
        console.error('Error:', error.response?.data || error.message);
        throw error;
    }
}