import FeatureBox from '@/components/feature-box'
import SearchArea from '@/components/search-area'

export function HomePage() {
  return (
    <main className="max-w-[1240px] w-full flex justify-between items-center mx-auto px-5">
      <div className="w-full flex flex-col">
        <SearchArea />

        <div>
          <h2 className="ml-8 my-6 text-2xl font-bold text-primary-foreground">Empresas parceiras</h2>
          {/* Carrossel com as empresas parceiras */}
        </div>

        <div>
          <h2 className="ml-8 my-6 text-2xl font-bold text-primary-foreground">Algumas features</h2>

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
