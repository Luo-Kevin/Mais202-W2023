export const linkFormatter = (link: string) => {
  try {
    const url = new URL(link);
    const searchParams = url.searchParams;
    const videoId: string | null = searchParams.get("v");
    return videoId;
  } catch (error) {
    console.log(error);
    return null;
  }
};
