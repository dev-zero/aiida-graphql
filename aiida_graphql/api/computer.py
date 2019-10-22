from enum import Enum

import strawberry


@strawberry.enum(name="SchedulerType")
class SchedulerType(Enum):
    DIRECT = "direct"
    PBSBASECLASS = "pbsbaseclasses.PbsBaseClass"
    PBSPRO = "pbspro"
    SGE = "sge"
    SLURM = "slurm"
    TORQUE = "torque"


@strawberry.enum(name="TransportType")
class TransportType(Enum):
    LOCAL = "local"
    SSH = "ssh"


@strawberry.type
class Computer:
    """Mirror of the AiiDA Computer ORM class"""

    uuid: strawberry.ID
    name: str
    hostname: str
    description: str
    scheduler_type: SchedulerType
    transport_type: TransportType

    @staticmethod
    def from_orm(ormobj):
        return Computer(
            uuid=ormobj[0].uuid,
            name=ormobj[0].name,
            hostname=ormobj[0].hostname,
            description=ormobj[0].description,
            scheduler_type=ormobj[0].get_scheduler_type(),
            transport_type=ormobj[0].get_transport_type(),
        )
