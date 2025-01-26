import { Button } from './ui/button'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from './ui/pagination'
import { VehicleBox } from './vehicle-box'

export function VehicleList() {
  return (
    <>
      <div className="w-full grid grid-cols-2 gap-3 mt-8">
        <VehicleBox />
        <VehicleBox />
        <VehicleBox />
        <VehicleBox />
        <VehicleBox />
        <VehicleBox />
      </div>

      <Pagination className="col-span-2 mt-8 text-primary-foreground">
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious href="#" />
          </PaginationItem>
          <PaginationItem>
            <PaginationLink href="#">1</PaginationLink>
            <PaginationLink href="#">2</PaginationLink>
          </PaginationItem>
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
          <PaginationItem>
            <PaginationNext href="#" />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </>
  )
}
