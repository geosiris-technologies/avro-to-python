// SPDX-FileCopyrightText: 2023 Geosiris
// SPDX-License-Identifier: Apache-2.0 OR MIT
use apache_avro::{Schema, AvroResult, to_avro_datum, to_value};
use std::time::{SystemTime, UNIX_EPOCH};
use std::fmt;
use std::io::Read;
use std::str::FromStr;
use enum_dispatch::enum_dispatch;

use crate::energistics::etp::v12::datatypes::version::Version;

pub fn time_to_etp(time: SystemTime) -> i64 {
    let since_the_epoch = time
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards");
    let in_ms = since_the_epoch.as_millis();
    return in_ms.try_into().unwrap();
}

#[derive(Debug, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
pub enum Role {
    All,
    Client,
    Server,
    Customer,
    Store,
    Producer,
    Consumer,
}

impl fmt::Display for Role{
     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Self::All => "*".to_string(),
                Self::Client => "client".to_string(),
                Self::Server => "server".to_string(),
                Self::Customer => "customer".to_string(),
                Self::Store => "store".to_string(),
                Self::Producer => "producer".to_string(),
                Self::Consumer => "consumer".to_string(),
            }
        )
    }
}

impl FromStr for Role {
    type Err = ();
    fn from_str(input: &str) -> Result<Role, Self::Err> {
        match input {
            "*" => Ok(Self::All),
            "client" => Ok(Self::Client),
            "server" => Ok(Self::Server),
            "customer" => Ok(Self::Customer),
            "store" => Ok(Self::Store),
            "producer" => Ok(Self::Producer),
            "consumer" => Ok(Self::Consumer),
            _ => Err(()),
        }
    }
}

pub const ETP12VERSION: Version = Version {
    major: 1,
    minor: 2,
    revision: 0,
    patch: 0,
};

pub const ETP11VERSION: Version = Version {
    major: 1,
    minor: 1,
    revision: 0,
    patch: 0,
};

#[enum_dispatch(ProtocolMessage)]
pub trait Schemable{
    fn avro_schema(&self) -> Option<Schema>;
    fn avro_schema_str(&self) -> &'static str;
}

#[enum_dispatch(ProtocolMessage)]
pub trait AvroSerializable: Schemable {
    fn avro_serialize(&self) -> AvroResult<Vec<u8>> 
        where Self: serde::Serialize + Schemable
    {
        let hdr_value = to_value(self).unwrap();
        return to_avro_datum(&self.avro_schema().unwrap(), hdr_value);
    }
}

pub trait AvroDeserializable {
    fn avro_deserialize<R: Read>(input: &mut R) -> AvroResult<Self> where Self: Sized; 
}

#[enum_dispatch(ProtocolMessage)]
pub trait ETPMetadata: AvroSerializable {

    fn protocol(&self) -> i32;
    fn message_type(&self) -> i32;
    fn sender_role(&self) -> Vec<Role>;
    fn protocol_roles(&self) -> Vec<Role>;
    fn multipart_flag(&self) -> bool;
}