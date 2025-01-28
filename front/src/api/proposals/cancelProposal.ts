import { api } from '@/lib/axios'

interface cancelProposalBody {
    id_proposta: number
    token: string | undefined
}

export async function cancelProposal({
    id_proposta,
    token
}: cancelProposalBody) {
    try {
        const response = await api.delete(
        `/propostas/cancelar_proposta/${id_proposta}`,
        {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        },
        )
        return response.data
    } catch (error : any) {
        console.error('Error:', error.response?.data || error.message)
        throw error
    }
}