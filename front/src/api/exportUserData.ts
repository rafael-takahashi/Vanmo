import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

export async function exportUserData() {
  try {
    const token = Cookies.get('auth_token')

    if (!token) {
      throw new Error('Token not found.')
    }

    const response = await api.get('/usuario/exportar_dados/csv', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      responseType: 'blob', 
    })

    // Create a URL for the blob
    const url = window.URL.createObjectURL(new Blob([response.data]))

    // Create a link element
    const link = document.createElement('a')
    link.href = url

    // Extract filename from content-disposition header
    const contentDisposition = response.headers['content-disposition']
    let filename = 'meus_dados.csv' // Default filename
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+)"?/)
      if (filenameMatch.length > 1) {
        filename = filenameMatch[1]
      }
    }

    link.setAttribute('download', filename)

    // Append to the document, click, and remove
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    // Clean up the URL object
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error exporting data:', error)
    throw new Error('Failed to export data. Please try again.')
  }
}
