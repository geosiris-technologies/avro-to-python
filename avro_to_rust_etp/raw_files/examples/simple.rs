// SPDX-FileCopyrightText: 2023 Geosiris
// SPDX-License-Identifier: Apache-2.0 OR MIT
use etptypes::energistics::etp::v12::protocol::core::ping::Ping;
use std::env;
use std::collections::HashMap;
use std::time::{SystemTime};
use serde_json;

use etptypes::energistics::etp::v12::datatypes::protocol::Protocol;
use etptypes::energistics::etp::v12::datatypes::supported_protocol::SupportedProtocol;
use etptypes::energistics::etp::v12::datatypes::endpoint_capability_kind::EndpointCapabilityKind;
use etptypes::energistics::etp::v12::protocol::core::request_session::RequestSession;
use etptypes::energistics::etp::v12::datatypes::uuid::random_uuid;
use etptypes::helpers::*;
use etptypes::error::*;


fn main() {
    env::set_var("RUST_BACKTRACE", "full");

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
        client_instance_id: random_uuid(),
        requested_protocols: protocols,
        supported_data_objects: vec![],
        supported_compression: vec!["gzip".to_string()],
        supported_formats: vec!["xml".to_string(), "json".to_string()],
        current_date_time: time_to_etp(now),
        earliest_retained_change_time: time_to_etp(now),
        server_authorization_required: false,
        endpoint_capabilities: HashMap::new(),
    };

    let ping = Ping{
        current_date_time: time_to_etp(now)
    };

    for s in EndpointCapabilityKind::iter() {
      println!("> {:?}", s);
    }

    println!("{:?}", rq);
    println!("{:?}", einvalid_messagetype());
    println!("{:?}", Protocol::Core);
    println!("{:?}", serde_json::from_str::<EndpointCapabilityKind>(r#""MaxWebSocketMessagePayloadSize""#).unwrap());
    println!("{:?}", serde_json::to_string_pretty(&EndpointCapabilityKind::ActiveTimeoutPeriod).unwrap());
    


    /* Ping */
    let record_a = ping.avro_serialize();
    match record_a{
        Err(ref e) => println!("{}", e),
        _ => {}
    }
    let record = record_a.unwrap();
    let mut record_slice = record.as_slice();
    println!("{:?}", record_slice);
    println!("{:?}", Ping::avro_deserialize(&mut record_slice));

    /* Request session */

    /*println!("{:?}", RequestSession::avro_schema_str());*/
    /*println!("{:?}", RequestSession::avro_schema());*/
    println!("{:?}", RequestSession::default());

    let record_a = rq.avro_serialize();
    match record_a{
        Err(ref e) => println!("{}", e),
        _ => {}
    }
    let record = record_a.unwrap();
    let mut record_slice = record.as_slice();
    println!("{:?}", record_slice);
    println!("{:?}", RequestSession::avro_deserialize(&mut record_slice));
    println!("{:?}", rq.as_protocol_message().avro_schema());
    println!("{:?}", rq.as_protocol_message().avro_serialize());
}
