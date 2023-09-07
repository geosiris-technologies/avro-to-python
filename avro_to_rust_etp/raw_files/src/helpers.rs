// SPDX-FileCopyrightText: 2023 Geosiris
// SPDX-License-Identifier: Apache-2.0 OR MIT
use avro_rs::{Codec, Schema, Writer};
use std::time::{SystemTime, UNIX_EPOCH};

use crate::energistics::etp::v12::datatypes::version::Version;

pub fn time_to_etp(time: SystemTime) -> i64 {
    let since_the_epoch = time
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards");
    let in_ms = since_the_epoch.as_millis();
    return in_ms.try_into().unwrap();
}

pub enum Role {
    All,
    Client,
    Server,
    Customer,
    Store,
    Producer,
    Consumer,
}

impl Role {
    pub fn to_string(self) -> String {
        match self {
            Self::All => "*".to_string(),
            Self::Client => "client".to_string(),
            Self::Server => "server".to_string(),
            Self::Customer => "customer".to_string(),
            Self::Store => "store".to_string(),
            Self::Producer => "producer".to_string(),
            Self::Consumer => "consumer".to_string(),
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

pub trait ETPMetadata {
    fn avro_schema() -> Option<Schema>;

    fn protocol(&self) -> i32;
    fn message_type(&self) -> i32;
    fn sender_role(&self) -> Vec<Role>;
    fn protocol_roles(&self) -> Vec<Role>;
    fn multipart_flag(&self) -> bool;

    fn avro_serialize(&self) -> Option<Vec<u8>> where Self: serde::Serialize{
        if let Some(schema) = Self::avro_schema(){
            let mut writer = Writer::with_codec(&schema, Vec::new(), Codec::Deflate);
            let _ = writer.append_ser(self);
            Some(writer.into_inner().unwrap())
        }else{
            None
        }
    }

    /*fn avro_deserialize<'de>(input: &Vec<u8>) -> Result<Self, Error> where Self: serde::Deserialize<'de> {
        let schema = Self::avro_schema()?;
        if let Some(result) = Reader::with_schema(&schema, &input[..])?.next(){
            /*match &result.next(){
                None => panic!("{:?}", "nothing to Deserialize")
                Some(x) => from_value::<Self>(&x.unwrap())
            }*/
            let value = result.unwrap();
            Ok(from_value::<Self>(&value).unwrap())
        }else{
            Err(None)

        }
        
    }
    fn avro_deserialize<'de>(input: &Vec<u8>) -> AvroResult<Self> where Self: serde::Deserialize<'de> {
        match Self::avro_schema(){
            Some(schema) => {
                let mut reader = Reader::with_schema(&schema, &input[..]).unwrap();
                let value = reader.next().unwrap();
                let val = value.unwrap();
                from_value(&val)
                /*match from_value::<'de ,Self>(&val){
                    Ok(result) => Some(result),
                    Err(_) => None
                }*/
            },
            None => None
        }
    }
*/
    /*fn avro_deserialize<'de>(input: &Vec<u8>) -> AvroResult<Self> where Self: serde::Deserialize<'de> {
        from_value::<'de ,Self>(&Reader::with_schema(&Self::avro_schema().unwrap(), &input[..]).unwrap().iter().collect().as_slice().unwrap()?.unwrap())
    }*/
}