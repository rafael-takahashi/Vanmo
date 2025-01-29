import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from './ui/accordion'

export function FaqArea() {
  return (
    <div className="w-full mt-14 bg-white p-8 rounded-md shadow-lg">
      <h2 className="text-2xl font-bold mb-2">
        Perguntas Respondidas Frequentemente
      </h2>
      <Accordion type="single" collapsible className="w-full">
        <AccordionItem value="item-1">
          <AccordionTrigger>O que é fretamento de ônibus?</AccordionTrigger>
          <AccordionContent>
            O fretamento de ônibus é a solução ideal para quem precisa de transporte seguro,
            confortável e eficiente para grupos. Seja para eventos, excursões, viagens
            corporativas ou turismo, oferecemos veículos modernos e motoristas experientes
            para garantir uma experiência tranquila.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-2">
          <AccordionTrigger>
            O que está incluído no valor do fretamento?
          </AccordionTrigger>
          <AccordionContent>
            O valor do fretamento inclui o aluguel do ônibus, o serviço de um motorista profissional,
            combustível, pedágios e seguro de viagem. Se houver necessidade de serviços extras, 
            como hospedagem do motorista ou alterações na rota, nossa equipe estará pronta para 
            ajustar conforme sua necessidade.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-3">
          <AccordionTrigger>
            O que fazer em caso de atraso ou imprevistos durante a viagem?
          </AccordionTrigger>
          <AccordionContent>
            Caso ocorra qualquer imprevisto, entre em contato imediatamente com nossa central de atendimento. 
            Nossa equipe está preparada para oferecer suporte rápido e garantir que sua viagem continue sem complicações.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-4">
          <AccordionTrigger>
            Como posso fazer uma reclamação ou dar um feedback sobre o serviço?
          </AccordionTrigger>
          <AccordionContent>
            Sua opinião é fundamental para nós! Para registrar uma reclamação ou enviar um feedback, 
            utilize nossos canais oficiais de atendimento: telefone, e-mail ou formulário no site. 
            Garantimos um retorno rápido e um compromisso com a melhoria contínua do nosso serviço.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  )
}
