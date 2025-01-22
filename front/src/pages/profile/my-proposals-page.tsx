import ProposalList from '@/components/proposal-list'
import SideMenuProfile from '@/components/side-menu-profile'

export default function MyProposalsPage() {
  return (
    <main className="grid grid-cols-3 gap-4 mt-20">
      <SideMenuProfile />

      <div className="col-span-2 bg-primary-foreground p-10 rounded-md">
        <ProposalList />
      </div>
    </main>
  )
}
