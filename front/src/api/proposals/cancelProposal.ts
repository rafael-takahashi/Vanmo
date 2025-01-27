import { api } from '@/lib/axios'

interface cancelProposalBody {
    id_proposta: number
    token: string | undefined
}

export async function cancelProposal({
    id_proposta,
    token
}: cancelProposalBody) {
    const jsonBody = JSON.stringify({
        id_proposta: id_proposta
    })
    try {
        const response = await api.put(
        `/propostas/cancelar_proposta/`,
        jsonBody,
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