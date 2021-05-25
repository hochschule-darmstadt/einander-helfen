import Radius from "@/models/radius";

import radiiData from "./radii.json";

const radii: Radius[] = radiiData as Radius[];
// now this object can not be changed anymore
Object.freeze(radii);

const getDefaultRadius = (): Radius => Object.assign({}, radii[0]);

export { getDefaultRadius };

export default radii;
