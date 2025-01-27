import 'swiper/css'
import Cookies from 'js-cookie'

import { MapPin } from '@phosphor-icons/react'
import { useNavigate } from 'react-router'
import { Swiper, SwiperSlide } from 'swiper/react'

import FeatureBox from '@/components/feature-box'
import SearchArea from '@/components/search-area'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

import garcia from '../assets/garcia.jpg'
import { getProposalData } from '@/api/proposals/getProposalData'
import { createProposal } from '@/api/proposals/createProposal'

export function HomePage() {

  const token = Cookies.get('auth_token')
  
  const tsDate = new Date();

  // Get the ISO string from the Date object
  const isoString = tsDate.toISOString(); // Returns a string like "2025-01-27T15:30:00.000Z"

  // Now you can safely use split on the string
  const dateOnly = isoString.split('T')[0]; // "2025-01-27"

  createProposal({id_empresa: 1,
    id_veiculo: 1,
    cidade_saida: 'Maringá',
    cidade_chegada: 'Curitiba',
    distancia_extra_km: 0,
    data_saida: dateOnly,
    data_chegada: dateOnly,
    token}).then((response) => {
    console.log(response)
  })

  const navigate = useNavigate()

  return (
    <main className="max-w-[1240px] w-full flex justify-between items-center mx-auto px-5">
      <div className="w-full flex flex-col">
        <SearchArea />

        <div className="w-full mt-10">
          <h2 className="text-2xl font-bold mb-2">Empresas Parceiras</h2>
          <Swiper spaceBetween={10} slidesPerView={4} loop={true}>
            <SwiperSlide>
              <Card
                onClick={() => navigate('/empresa/viacao+garcia')}
                className="cursor-pointer"
              >
                <CardHeader className="text-center">
                  <CardTitle className="text-xl">Viacao Garcia</CardTitle>
                </CardHeader>
                <CardContent>
                  <img src={garcia} alt="" className="rounded-md " />
                  <span className="flex mt-2 gap-1">
                    <MapPin size={24} weight="fill" /> Maringá-PR
                  </span>
                </CardContent>
              </Card>
            </SwiperSlide>
            <SwiperSlide>
              <Card
                onClick={() => navigate('/empresa/viacao+garcia')}
                className="cursor-pointer"
              >
                <CardHeader className="text-center">
                  <CardTitle className="text-xl">Viacao Garcia</CardTitle>
                </CardHeader>
                <CardContent>
                  <img src={garcia} alt="" className="rounded-md " />
                  <span className="flex mt-2 gap-1">
                    <MapPin size={24} weight="fill" /> Maringá-PR
                  </span>
                </CardContent>
              </Card>
            </SwiperSlide>
            <SwiperSlide>
              <Card
                onClick={() => navigate('/empresa/viacao+garcia')}
                className="cursor-pointer"
              >
                <CardHeader className="text-center">
                  <CardTitle className="text-xl">Viacao Garcia</CardTitle>
                </CardHeader>
                <CardContent>
                  <img src={garcia} alt="" className="rounded-md " />
                  <span className="flex mt-2 gap-1">
                    <MapPin size={24} weight="fill" /> Maringá-PR
                  </span>
                </CardContent>
              </Card>
            </SwiperSlide>
            <SwiperSlide>
              <Card
                onClick={() => navigate('/empresa/viacao+garcia')}
                className="cursor-pointer"
              >
                <CardHeader className="text-center">
                  <CardTitle className="text-xl">Viacao Garcia</CardTitle>
                </CardHeader>
                <CardContent>
                  <img src={garcia} alt="" className="rounded-md " />
                  <span className="flex mt-2 gap-1">
                    <MapPin size={24} weight="fill" /> Maringá-PR
                  </span>
                </CardContent>
              </Card>
            </SwiperSlide>
            <SwiperSlide>
              <Card
                onClick={() => navigate('/empresa/viacao+garcia')}
                className="cursor-pointer"
              >
                <CardHeader className="text-center">
                  <CardTitle className="text-xl">Viacao Garcia</CardTitle>
                </CardHeader>
                <CardContent>
                  <img src={garcia} alt="" className="rounded-md " />
                  <span className="flex mt-2 gap-1">
                    <MapPin size={24} weight="fill" /> Maringá-PR
                  </span>
                </CardContent>
              </Card>
            </SwiperSlide>
          </Swiper>
        </div>

        <div className="w-full mt-10">
          <h2 className="text-2xl font-bold mb-2">Algumas Features</h2>

          <div className="grid grid-cols-2 gap-4">
            <FeatureBox />
            <FeatureBox />
            <FeatureBox />
            <FeatureBox />
          </div>
        </div>
      </div>
    </main>
  )
}
