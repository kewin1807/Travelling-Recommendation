import React from "react";
import RoomFilter from "./RoomFilter";
import RoomList from "./RoomList";
import { withRoomConsumer } from "../Context";
import Loading from "./Loading";
import TourList from "./TourList"
import Pagination from "react-js-pagination";

function RoomContainer({ context }) {
  const { loading, featuredRooms, rooms, paginatedRooms, paginatedTours, totalItemRooms, totalItemTours, itemsCountPerPage, handlePageChangeRoom, handlePageChangeTour, currentPageRoom, currentPageTour } = context;
  // console.log(context);
  if (loading) {
    return <Loading />;
  }
  return (
    <div>
      <RoomFilter rooms={rooms} />
      <RoomList rooms={paginatedRooms} />
      {totalItemRooms > 1 ?
        <div style={{
          flex: 1, marginLeft: 600,
        }}>

          <Pagination itemClass="page-item"
            linkClass="page-link"
            activePage={currentPageRoom}
            itemsCountPerPage={itemsCountPerPage}
            totalItemsCount={totalItemRooms}
            pageRangeDisplayed={5}
            onChange={handlePageChangeRoom}
          />
        </div> : null}


      <TourList tours={paginatedTours} />
      {totalItemTours > 1 ?
        <div style={{
          flex: 1, marginLeft: 600
        }}>
          <Pagination itemClass="page-item"
            linkClass="page-link"
            activePage={currentPageTour}
            itemsCountPerPage={itemsCountPerPage}
            totalItemsCount={totalItemTours}
            pageRangeDisplayed={5}
            onChange={handlePageChangeTour}
          />
        </div> : null}
    </div>
  );
}

export default withRoomConsumer(RoomContainer);

// export default function RoomsContainer() {
//   return (
//     <RoomConsumer>
//       {value => {
//         console.log(value);
//         const { loading, sortedRooms, rooms } = value;
//         if (loading) {
//           return <Loading />;
//         }
//         return (
//           <div>
//             Hello from Room Containter
//             <RoomFilter rooms={rooms} />
//             <RoomList rooms={sortedRooms} />
//           </div>
//         );
//       }}
//     </RoomConsumer>
//   );
// }
