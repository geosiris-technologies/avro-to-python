// SPDX-FileCopyrightText: 2023 Geosiris
// SPDX-License-Identifier: Apache-2.0 OR MIT

use etptypes::energistics::etp::v12::datatypes::endpoint_capability_kind::EndpointCapabilityKind;
use etptypes::energistics::etp::v12::datatypes::object::context_info::ContextInfo;
use etptypes::energistics::etp::v12::datatypes::object::context_scope_kind::ContextScopeKind;
use etptypes::energistics::etp::v12::datatypes::object::relationship_kind::RelationshipKind;
use etptypes::energistics::etp::v12::protocol::discovery::get_resources::GetResources;
use etptypes::helpers::AvroDeserializable;
use etptypes::helpers::AvroSerializable;
use std::str::FromStr;


#[test]
fn test_from_and_to() {
	for cap_kind in EndpointCapabilityKind::iter(){
        assert_eq!(cap_kind, &EndpointCapabilityKind::from_str(format!("{}", cap_kind).as_str()).unwrap());
    }

}

#[test]
fn test_get_resources_serialization(){
    let getress = GetResources::default_with_params(
        ContextInfo { 
            uri:"eml:///".to_string(),
            depth:1 as i32,
            data_object_types:vec![],
            navigable_edges: RelationshipKind::Both,
            include_secondary_targets: false,
            include_secondary_sources: false,
        },
        ContextScopeKind::Self_,
        None, None
    );
    let record_a = getress.avro_serialize();
    assert!(record_a.is_ok());

    match record_a {
        Err(ref e) => println!("{}", e),
        _ => {}
    }
    let record = record_a.unwrap();
    let mut record_slice = record.as_slice();
    let result = GetResources::avro_deserialize(&mut record_slice);

    assert!(result.is_ok());
}
