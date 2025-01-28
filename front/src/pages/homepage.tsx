import 'swiper/css'

import { MapPin } from '@phosphor-icons/react'
import { useNavigate, useSearchParams } from 'react-router'
import { Swiper, SwiperSlide } from 'swiper/react'

import FeatureBox from '@/components/feature-box'
import SearchArea from '@/components/search-area'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

import garcia from '../assets/garcia.jpg'

export function HomePage() {
  const navigate = useNavigate()

  function handleNavigate(name: string) {
    navigate(`/empresa/${name}`)
  }

  return (
    <main className="max-w-[1240px] w-full flex justify-between items-center mx-auto px-5">
      <div className="w-full flex flex-col">
        <SearchArea />

        <div className="w-full mt-10">
          <h2 className="text-2xl font-bold mb-2">Empresas Parceiras</h2>
          <Swiper spaceBetween={10} slidesPerView={4} loop={true}>
            <SwiperSlide>
              <Card
                onClick={() => handleNavigate('1')}
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
                onClick={() => handleNavigate('1')}
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
                onClick={() => handleNavigate('1')}
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
                onClick={() => handleNavigate('1')}
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
                onClick={() => handleNavigate('1')}
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
