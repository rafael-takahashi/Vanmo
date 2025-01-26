import { api } from '@/lib/axios'

interface deleteUserHeader {
  token: string | undefined
}

export async function deleteUser({ token }: deleteUserHeader) {
    try {
        const response = await api.delete('/usuario/apagar_conta', {
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