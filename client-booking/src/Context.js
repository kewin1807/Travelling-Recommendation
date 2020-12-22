import React, { Component } from "react";
import { post } from "../src/api"
// import items from "./data";
// import Client from "./Contentful";

const RoomContext = React.createContext();

class RoomProvider extends Component {
  state = {
    rooms: [],
    tours: [],
    featuredRooms: [],
    paginatedRooms: [],
    paginatedTours: [],
    loading: false,
    province: "Chọn điểm đến",
    latitude: "",
    longitude: "",
    type_price_hotel: "-1",
    type_price_tour: "-1",
    currentPageRoom: 1,
    currentPageTour: 1,
    totalItemRooms: 0,
    totalItemTours: 0,
    itemsCountPerPage: 8,
    totalPageRooms: 0,
    totalPageTours: 0
  };

  // getData ** TODO
  getData = async (city_id, type_price_hotel, type_price_tour) => {
    this.setState({ loading: true })
    try {
      const res = await post("/api/recommendation", { data: { "city_id": city_id, "type_price_hotel": type_price_hotel, "type_price_tour": type_price_tour } })
      const rooms = res.hotels
      const tours = res.tours
      let paginatedRooms = []
      let paginatedTours = []
      let totalPageRooms = 0
      let totalPageTours = 0
      let totalItemRooms = 0
      let totalItemTours = 0
      if (rooms.length != 0) {
        totalItemRooms = rooms.length
        totalPageRooms = Math.ceil(rooms.length / this.state.itemsCountPerPage)
        if (totalPageRooms <= 1) {
          paginatedRooms = rooms
        }
        else {
          paginatedRooms = rooms.slice(0, this.state.itemsCountPerPage - 1)
        }
      }
      if (tours.length != 0) {
        totalItemTours = tours.length
        totalPageTours = Math.ceil(tours.length / this.state.itemsCountPerPage)
        if (totalPageTours <= 1) {
          paginatedTours = tours
        }
        else {
          paginatedTours = tours.slice(0, this.state.itemsCountPerPage - 1)
        }
      }
      this.setState({ rooms, tours, paginatedTours, paginatedRooms, totalItemRooms, totalItemTours, loading: false })

      // let rooms = this.formatData(response.items);
      // let featuredRooms = rooms.filter(room => room.featured === true);
      // let maxPrice = Math.max(...rooms.map(item => item.price));
      // let maxSize = Math.max(...rooms.map(item => item.size));
      // this.setState({
      //   rooms,
      //   featuredRooms,
      //   sortedRooms: rooms,
      //   loading: false,
      //   maxPrice,
      //   maxSize
      // });
    } catch (error) {
      console.log(error);
    }
  };

  handleChange = async event => {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = event.target.name;
    this.setState(
      {
        [name]: value
      },
      await this.filterRooms
    );
  };

  filterRooms = async () => {
    let {
      province,
      type_price_hotel,
      type_price_tour
    } = this.state;
    if (province === "Chọn điểm đến") {
      alert("Bạn chưa chọn điểm đến")
    }
    else {
      await this.getData(province,
        type_price_hotel,
        type_price_tour)
    }
  };

  handlePageChangeRoom = (pageNumber) => {
    let paginatedRooms = []
    if (pageNumber < this.state.totalItemRooms) {
      paginatedRooms = this.state.rooms.slice((pageNumber - 1) * this.state.itemsCountPerPage, pageNumber * this.state.itemsCountPerPage)
    }
    else {
      paginatedRooms = this.state.rooms.slice((pageNumber - 1) * this.state.itemsCountPerPage, this.state.rooms.length)
    }

    this.setState({ currentPageRoom: pageNumber, paginatedRooms: paginatedRooms });
  }

  handlePageChangeTour = (pageNumber) => {
    let paginatedTours = []
    if (pageNumber < this.state.totalItemTours) {
      paginatedTours = this.state.tours.slice((pageNumber - 1) * this.state.itemsCountPerPage, pageNumber * this.state.itemsCountPerPage)
    }
    else {
      paginatedTours = this.state.tours.slice((pageNumber - 1) * this.state.itemsCountPerPage, this.state.tours.length)
    }

    this.setState({ currentPageTour: pageNumber, paginatedTours: paginatedTours });
  }

  render() {
    return (
      <RoomContext.Provider
        value={{
          ...this.state,
          handlePageChangeRoom: this.handlePageChangeRoom,
          handlePageChangeTour: this.handlePageChangeTour,
          handleChange: this.handleChange
        }}
      >
        {this.props.children}
      </RoomContext.Provider>
    );
  }
}

const RoomConsumer = RoomContext.Consumer;

export function withRoomConsumer(Component) {
  return function ConsumerWrapper(props) {
    return (
      <RoomConsumer>
        {value => <Component {...props} context={value} />}
      </RoomConsumer>
    );
  };
}

export { RoomProvider, RoomConsumer, RoomContext };
