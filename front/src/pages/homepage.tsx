import 'swiper/css'

import { MapPin } from '@phosphor-icons/react'
import { useNavigate, useSearchParams } from 'react-router'
import { Swiper, SwiperSlide } from 'swiper/react'

import FeatureBox from '@/components/feature-box'
import SearchArea from '@/components/search-area'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
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
        <div className="mt-16">
          <SearchArea />
        </div>

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
          <h2 className="text-2xl font-bold mb-2">FAQ</h2>
          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="item-1">
              <AccordionTrigger>O que é fretamento de ônibus?</AccordionTrigger>
              <AccordionContent>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry's standard dummy
                text ever since the 1500s, when an unknown printer took a galley
                of type and scrambled it to make a type specimen book.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="item-2">
              <AccordionTrigger>
                O que está incluído no valor do fretamento?
              </AccordionTrigger>
              <AccordionContent>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry's standard dummy
                text ever since the 1500s, when an unknown printer took a galley
                of type and scrambled it to make a type specimen book.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="item-3">
              <AccordionTrigger>
                O que fazer em caso de atraso ou imprevistos durante a viagem?
              </AccordionTrigger>
              <AccordionContent>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry's standard dummy
                text ever since the 1500s, when an unknown printer took a galley
                of type and scrambled it to make a type specimen book.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="item-4">
              <AccordionTrigger>
                Como posso fazer uma reclamação ou dar um feedback sobre o
                serviço?
              </AccordionTrigger>
              <AccordionContent>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry's standard dummy
                text ever since the 1500s, when an unknown printer took a galley
                of type and scrambled it to make a type specimen book.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
    </main>
  )
}
