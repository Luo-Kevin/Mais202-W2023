import axios from "axios";
import bodyProps from "../models/models";
const base_url: string = "http://localhost:8000";

export const model = async ({ link }: bodyProps) => {
  try {
    const response = await axios.get(`${base_url}/model/${link}`);
    const data = await response.data;
    // console.log(data);
    return data;
  } catch (error) {
    console.log(error);
    return "-1";
  }
};
