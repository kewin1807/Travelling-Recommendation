import React, { Component } from "react";
import {post } from "../src/api"
// import items from "./data";
// import Client from "./Contentful";

const RoomContext = React.createContext();

class RoomProvider extends Component {
  state = {
    rooms: [],
    tours: [],
    sortedRooms: [],
    featuredRooms: [],
    loading: false,
    province: "Chọn điểm đến",
    capacity: 1,
    price: 0,
    minPrice: 0,
    maxPrice: 0,
    minSize: 0,
    maxSize: 0,
    breakfast: false,
    pets: false
  };

  // getData ** TODO
  getData = async (city_id) => {
    this.setState({ loading: true })
    try {

      const res = await post("/api/recommendation", { data: { "city_id": city_id } })

      this.setState({ rooms: res.hotels, loading: false, tours: res.tours })
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
    } = this.state;
    if (province === "Chọn điểm đến") {
      alert("Bạn chưa chọn điểm đến")
    }
    else {
      await this.getData(province)
    }
  };

  render() {
    return (
      <RoomContext.Provider
        value={{
          ...this.state,
          getRoom: this.getRoom,
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
