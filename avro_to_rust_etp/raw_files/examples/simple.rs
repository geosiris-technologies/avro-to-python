// SPDX-FileCopyrightText: 2023 Geosiris
// SPDX-License-Identifier: Apache-2.0 OR MIT
use std::env;
use std::collections::HashMap;
use std::time::{SystemTime};
use serde_json;

use etptypes::energistics::etp::v12::datatypes::protocol::Protocol;
use etptypes::energistics::etp::v12::datatypes::supported_protocol::SupportedProtocol;
use etptypes::energistics::etp::v12::datatypes::endpoint_capability_kind::EndpointCapabilityKind;
use etptypes::energistics::etp::v12::protocol::core::request_session::RequestSession;
use etptypes::energistics::etp::v12::datatypes::uuid::Uuid;
use etptypes::helpers::*;
use etptypes::error::*;


fn test_trait<T: ETPMetadata>(obj: &T) {
    println!(
        "Protocol {:?}; Messagetype {:?}",
        obj.protocol(),
        obj.message_type()
    );
}

fn main() {
    env::set_var("RUST_BACKTRACE", "1");

    let protocols = vec![
    SupportedProtocol{
        protocol: Protocol::Core as i32,
        protocol_version: ETP12VERSION,
        role: "Server".to_string(),
        protocol_capabilities: HashMap::new()
    },
    SupportedProtocol{
        protocol: 3,
        protocol_version: ETP12VERSION,
        role: "Server".to_string(),
        protocol_capabilities: HashMap::new()
    },
    SupportedProtocol{
        protocol: 4,
        protocol_version: ETP12VERSION,
        role: "Server".to_string(),
        protocol_capabilities: HashMap::new()
    }
    ];

    let now = SystemTime::now(); 

    let rq = RequestSession {
        application_name: "etp-rs Client Library Application".to_string(),
        application_version: "0.1".to_string(),
        client_instance_id: Uuid::new_v4(),
        requested_protocols: protocols,
        supported_data_objects: vec![],
        supported_compression: vec!["gzip".to_string()],
        supported_formats: vec!["xml".to_string(), "json".to_string()],
        current_date_time: time_to_etp(now),
        earliest_retained_change_time: time_to_etp(now),
        server_authorization_required: false,
        endpoint_capabilities: HashMap::new(),
    };

    for s in EndpointCapabilityKind::iter() {
      println!("> {:?}", s);
    }

    println!("{:?}", rq);
    println!("{:?}", einvalid_messagetype());
    println!("{:?}", Protocol::Core);
    println!("{:?}", serde_json::from_str::<EndpointCapabilityKind>(r#""MaxWebSocketMessagePayloadSize""#).unwrap());
    println!("{:?}", serde_json::to_string_pretty(&EndpointCapabilityKind::ActiveTimeoutPeriod).unwrap());
    println!("{:?}", RequestSession::default());

    test_trait(&rq);
    // let schemata: Vec<Schema> = Schema::parse_list(&ETP_SCHEMA_EMBED)
    // println!("{:?}", schemata);
    // println!("==========\n\n{:?}", rq.avro_serialize());
    // println!("==========\n\n{:?}", rq.avro_serialize());
}
