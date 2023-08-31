#![allow(dead_code)]

use crate::energistics::etp::v12::datatypes::error_info::ErrorInfo;

pub fn enorole() -> ErrorInfo{
	ErrorInfo{
		code: 1,
		message: r#"The server does not support the requested role."#.to_string(),
	}
}

pub fn enosupportedprotocols() -> ErrorInfo{
	ErrorInfo{
		code: 2,
		message: r#"The server does not support any of the requested protocols."#.to_string(),
	}
}

pub fn einvalid_messagetype() -> ErrorInfo{
	ErrorInfo{
		code: 3,
		message: r#"The message type ID is either: 1) not defined at all in the ETP Specification (e.g., no schema for it); or 2) not a correct message type ID for the receiving role (EXAMPLE: Per this specification, only the store role may SEND a GetDataObjectsResponse message; if the store RECEIVES a GetDataObjectsResponse message, it MUST send this error code.)"#.to_string(),
	}
}

pub fn eunsupported_protocol() -> ErrorInfo{
	ErrorInfo{
		code: 4,
		message: r#"The endpoint does not support the protocol identified in a message header."#.to_string(),
	}
}

pub fn einvalid_argument() -> ErrorInfo{
	ErrorInfo{
		code: 5,
		message: r#"Logically invalid argument. Use this error code in any situation where a logically invalid argument is encountered."#.to_string(),
	}
}

pub fn erequest_denied() -> ErrorInfo{
	ErrorInfo{
		code: 6,
		message: r#"The receiving endpoint has denied the request. RECOMMENDATION: Endpoints should supply an error message explaining why the request was denied. (EXAMPLE: If a customer attempts to change immutable fields in a data object, the store should send EREQUEST_DENIED, and the message could be "Cannot change the unit of measure for a channel".)"#.to_string(),
	}
}

pub fn enotsupported() -> ErrorInfo{
	ErrorInfo{
		code: 7,
		message: r#"The endpoint does not support the operation."#.to_string(),
	}
}

pub fn einvalid_state() -> ErrorInfo{
	ErrorInfo{
		code: 8,
		message: r#"Indicates that the message is not allowed in the current state of the protocol. EXAMPLE: In Protocol 21, a customer sending a SubscribeChannels message for a channel that the customer is already subscribed to, or receiving a message that is not applicable for the current operation (as defined in this specification)."#.to_string(),
	}
}

pub fn einvalid_uri() -> ErrorInfo{
	ErrorInfo{
		code: 9,
		message: r#"The URI sent is either a malformed URI, is not a valid URI format for ETP, or is not appropriate for specific requirements of a field in a message. EXAMPLE: If a customer sends an alternate URI format to a store that does not accept/support alternate URIs, the store MUST send this error code."#.to_string(),
	}
}

pub fn eauthorization_expired() -> ErrorInfo{
	ErrorInfo{
		code: 10,
		message: r#"Sent from server to client when the server is about to terminate the session because of an expired authorization."#.to_string(),
	}
}

pub fn enot_found() -> ErrorInfo{
	ErrorInfo{
		code: 11,
		message: r#"Used when a resource, a data object, part or range is not found. May be used in any situation, as appropriate."#.to_string(),
	}
}

pub fn elimit_exceeded() -> ErrorInfo{
	ErrorInfo{
		code: 12,
		message: r#"Sent by either endpoint if a request, response, or notification exceeds allowed or stated limits specified by the other endpoint when a more specific error code has not been specified.
EXAMPLES:
- In Protocol 13 (DataArray) if the customer attempts to put an array into the store that exceeds the store's MaxDataArraySize capability.
- In Protocol 21 (ChannelSubscribe) if a customer exceeds a store's value for MaxStreamingChannelsSessionCount capability."#.to_string(),
	}
}


pub fn ecompression_notsupported() -> ErrorInfo{
	ErrorInfo{
		code: 13,
		message: r#"Sent by either endpoint when it receives a message whose MessageHeader has a protocolId field = 0 AND whose message body is compressed. (That is, messages defined and used in Core (Protocol 0) MUST NEVER be compressed.)"#.to_string(),
	}
}

pub fn einvalid_object() -> ErrorInfo{
	ErrorInfo{
		code: 14,
		message: r#"Sent in any protocol when either role sends an invalid XML document. NOTE: ETP does not distinguish between malformed and well-formed but invalid for this purpose. The same error message is used in both cases."#.to_string(),
	}
}

pub fn emax_transactions_exceeded() -> ErrorInfo{
	ErrorInfo{
		code: 15,
		message: r#" The maximum number of transactions per ETP session has been exceeded. Currently, Transaction (Protocol 18) is the only ETP protocol that has the notion of a "transaction" and allows only 1 transaction per session."#.to_string(),
	}
}

pub fn edataobjecttype_notsupported() -> ErrorInfo{
	ErrorInfo{
		code: 16,
		message: r#"The data object type is not supported by the endpoint or was not negotiated for use during the current ETP session."#.to_string(),
	}
}

pub fn emaxsize_exceeded() -> ErrorInfo{
	ErrorInfo{
		code: 17,
		message: r#"Sent from a store to a customer when the customer attempts a get or put operation that exceeds the store's maximum advertised values for MaxDataObjectSize, MaxPartSize, or MaxDataArraySize capabilities."#.to_string(),
	}
}

pub fn emultipart_cancelled() -> ErrorInfo{
	ErrorInfo{
		code: 18,
		message: r#"Sent by either role to notify of canceled transmission of multipart response or request. EXAMPLE: When an endpoint's advertised value for the MaxConcurrentMultipart endpoint capability has been exceeded."#.to_string(),
	}
}

pub fn einvalid_message() -> ErrorInfo{
	ErrorInfo{
		code: 19,
		message: r#"Sent by either role when it is unable to de-serialize the header or body of a message."#.to_string(),
	}
}

pub fn einvalid_indexkind() -> ErrorInfo{
	ErrorInfo{
		code: 20,
		message: r#"Sent by either role when an index kind used in a message is invalid for the data."#.to_string(),
	}
}

pub fn enosupportedformats() -> ErrorInfo{
	ErrorInfo{
		code: 21,
		message: r#"The server does not support any of the client's supported formats."#.to_string(),
	}
}

pub fn erequestuuid_rejected() -> ErrorInfo{
	ErrorInfo{
		code: 22,
		message: r#"Sent by the store when it rejects a customer-assigned request UUID (requestUuid), most likely because the request UUID is not unique."#.to_string(),
	}
}

pub fn eupdategrowingobject_denied() -> ErrorInfo{
	ErrorInfo{
		code: 23,
		message: r#"Sent by a store when a customer tries to update an existing growing data object (i.e., do a put operation) using Store (Protocol 4) or includes parts when updating a growing data object header using GrowingObject (Protocol 6)."#.to_string(),
	}
}

pub fn ebackpressure_limit_exceeded() -> ErrorInfo{
	ErrorInfo{
		code: 24,
		message: r#"If the sender's queuing capacity is exhausted and it is imminently unable to send a message to the receiver, the sender MUST attempt to send this error and then attempt to send the CloseSession message. Sender MUST then close the connection, regardless of whether or not the ProtocolException and CloseSession messages were sent."#.to_string(),
	}
}

pub fn ebackpressure_warning() -> ErrorInfo{
	ErrorInfo{
		code: 25,
		message: r#"If sender starts to detect sending backpressure (e.g., queues of outgoing messages are starting to fill up), sender MAY send this warning."#.to_string(),
	}
}

pub fn etimed_out() -> ErrorInfo{
	ErrorInfo{
		code: 26,
		message: r#"May be sent by either role to cancel an operation when the response time for a relevant operation is exceeded, such as ResponseTimeoutPeriod or MultipartMessageTimeoutPeriod capabilities."#.to_string(),
	}
}

pub fn eauthorization_required() -> ErrorInfo{
	ErrorInfo{
		code: 27,
		message: r#"Sent from an endpoint during session negotiation (and ONLY during session negotiation) to indicate that the other endpoint requires authorization."#.to_string(),
	}
}

pub fn eauthorization_expiring() -> ErrorInfo{
	ErrorInfo{
		code: 28,
		message: r#"Optionally sent from an endpoint when the other endpoint's authorization will expire soon. The receiving endpoint should follow the necessary authorization workflow to renew its authorization. If it does not, the sending endpoint will eventually terminate the connection. The precise definition of "soon" and the required re-authorization workflow are intentionally out of the scope of the ETP Specification."#.to_string(),
	}
}

pub fn enosupporteddataobjecttypes() -> ErrorInfo{
	ErrorInfo{
		code: 29,
		message: r#"The server does not support any of the client's supported data object types."#.to_string(),
	}
}

pub fn eresponsecount_exceeded() -> ErrorInfo{
	ErrorInfo{
		code: 30,
		message: r#"Sent by a store endpoint to terminate a non-map response once the number of responses sent has reached the allowed or stated limits specified by the relevant capabilities. This lets customers know that the store has more data than it could return to the customer.
EXAMPLES:
- In Protocol 3 (Discovery) and all query protocols, sent by the store if it must stop sending responses to the customer because it has already sent MaxResponseCount responses to a customer request.
- In Protocol 21 (ChannelSubscribe), sent by the store if it must stop sending data points to a customer in response to a GetRanges request because the store has already sent MaxRangeDataItemCount data points in response to the request."#.to_string(),
	}
}

pub fn einvalid_append() -> ErrorInfo{
	ErrorInfo{
		code: 31,
		message: r#"Sent in response to a ChannelData message that is not appending data to a channel."#.to_string(),
	}
}

pub fn einvalid_operation() -> ErrorInfo{
ErrorInfo{
		code: 32,
		message: r#"Sent in response to a request when the requested operation would be invalid. EXAMPLE: In Protocol 6 (GrowingObject), a ReplacePartsByRange message where some replacement parts are not covered by the delete range is an invalid operation."#.to_string(),
	}
}

pub fn einvalid_channelid() -> ErrorInfo{
ErrorInfo{
		code: 1002,
		message: r#"Sent by either role when operations are requested on a channel ID that is not valid for the session. 4003 ENOCASCADE_DELETE Sent when an attempt is made to delete an object that has children and the store does not support cascading deletes (prune operations)."#.to_string(),
	}
}

pub fn eplural_object() -> ErrorInfo{
ErrorInfo{
		code: 4004,
		message: r#"Sent when an endpoint attempts put operations for more than one data object under the plural root of a 1.x Energistics data object. ETP only supports a single data object, one XML document. ETP 1.2 is not designed to work with 1.x Energistics data objects, but this error code is left for use with custom protocols."#.to_string(),
	}
}

pub fn eretention_period_exceeded() -> ErrorInfo{
ErrorInfo{
		code: 5001,
		message: r#"Sent from a store to a customer when the client asks for changes beyond the stated change period of a server."#.to_string(),
	}
}

pub fn enotgrowingobject() -> ErrorInfo{
ErrorInfo{
		code: 6001,
		message: r#"Sent from a store to a customer when the customer attempts to perform a growing object operation on an object that is not defined as a growing data object type. EXAMPLE: A store would send this if the customer attempted to add parts to a WITSML well object, which is not a growing data object."#.to_string(),
	}
}