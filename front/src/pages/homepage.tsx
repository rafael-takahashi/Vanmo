import 'swiper/css'

import { MapPin } from '@phosphor-icons/react'
import { useQuery } from '@tanstack/react-query'
import { format } from 'date-fns'
import { useNavigate } from 'react-router'
import { Swiper, SwiperSlide } from 'swiper/react'

import { fetchBusinessByFilters } from '@/api/fetchBusinessByFilters'
import { FaqArea } from '@/components/faq-area'
import SearchArea from '@/components/search-area'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

import garcia from '../assets/garcia.jpg'

export function HomePage() {
  const navigate = useNavigate()

  function handleNavigate(name: number) {
    navigate(`/empresa/${name}`)
  }
  const date1980 = format(new Date('1980-05-15'), 'yyyy-MM-dd')

  const { data, isLoading } = useQuery({
    queryKey: ['homepage'],
    queryFn: () =>
      fetchBusinessByFilters({
        local_partida: 'Maringá, PR',
        data_de_partida: date1980,
        pagina: 1,
        qtd_passageiros: '1',
      }),
  })

  return (
    <main className="max-w-[1240px] w-full flex justify-between items-center mx-auto px-5">
      <div className="w-full flex flex-col">
        <div className="mt-16">
          <SearchArea />
        </div>

        <div className="w-full mt-10">
          <h2 className="text-2xl font-bold mb-2">Empresas Parceiras</h2>
          {isLoading && (
            <>
              <Skeleton className="w-full h-[240px]" />
            </>
          )}

          {data && (
            <Swiper spaceBetween={10} slidesPerView={4} loop={true}>
              {data.map((empresa) => (
                <SwiperSlide key={empresa.id_usuario}>
                  {/* <Card
                    onClick={() => handleNavigate('1')}
                    className="cursor-pointer"
                  >
                    <CardHeader className="text-center">
                      <CardTitle className="text-xl">
                        {empresa.nome_fantasia}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <img src={garcia} alt="" className="rounded-md " />
                      <span className="flex mt-2 gap-1">
                        <MapPin size={24} weight="fill" />{' '}
                        {empresa.endereco.cidade}-{empresa.endereco.uf}
                      </span>
                    </CardContent>
                  </Card> */}

                  <div
                    onClick={() => handleNavigate(empresa.id_usuario)}
                    className="cursor-pointer text-primary-foreground"
                  >
                    <img src={garcia} alt="" className="rounded-t-md " />
                    <div className="flex items-center justify-between mt-1">
                      <h3 className="font-bold text-2xl">
                        {empresa.nome_fantasia}
                      </h3>
                      <span className="flex gap-1 text-sm">
                        <MapPin
                          size={18}
                          weight="fill"
                          color={'hsl(20 99% 65%)'}
                        />{' '}
                        {empresa.endereco.cidade}-{empresa.endereco.uf}
                      </span>
                    </div>
                  </div>
                </SwiperSlide>
              ))}
            </Swiper>
          )}
        </div>

        <FaqArea />
      </div>
    </main>
  )
}
