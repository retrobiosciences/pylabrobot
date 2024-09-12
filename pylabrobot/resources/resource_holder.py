from typing import Optional
from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.resource import Resource

def get_child_location(resource: Resource) -> Coordinate:
  """
  If a resource is rotated, its rotated around its local origin. This does not always
  match up with the parent resource's origin. This function calculates the difference
  between the two origins and calculates the location of the resource correctly.
  """
  if not resource.rotation.y == resource.rotation.x == 0:
    raise ValueError("Resource rotation must be 0 around the x and y axes")
  if not resource.rotation.z % 90 == 0:
    raise ValueError("Resource rotation must be a multiple of 90 degrees on the z axis")
  location = {
    0.0: Coordinate(x=0, y=0, z=0),
    90.0: Coordinate(x=resource.get_size_y(), y=0, z=0),
    180.0: Coordinate(x=resource.get_size_y(), y=resource.get_size_x(), z=0),
    270.0: Coordinate(x=0, y=resource.get_size_x(), z=0),
  }[resource.rotation.z % 360]
  return location

class ResourceHolderMixin:
  """
  A mixin class for resources that can hold other resources, like a plate or a lid
  """

  def assign_child_resource(
    self,
    resource: Resource,
    location: Optional[Coordinate] = None,
    reassign: bool = True
  ):
    location = get_child_location(resource) + (location or Coordinate.zero())
    # mypy doesn't play well with the Mixin pattern
    return super().assign_child_resource(resource, location, reassign) # type: ignore
