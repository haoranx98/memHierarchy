// Copyright 2009-2023 NTESS. Under the terms
// of Contract DE-NA0003525 with NTESS, the U.S.
// Government retains certain rights in this software.
//
// Copyright (c) 2009-2023, NTESS
// All rights reserved.
//
// Portions are copyright of other developers:
// See the file CONTRIBUTORS.TXT in the top level directory
// of the distribution for more information.
//
// This file is part of the SST software package. For license
// information, see the LICENSE file in the top level directory of the
// distribution.


#include <sst_config.h>
#include <sst/core/link.h>
#include "sst/elements/memHierarchy/util.h"
#include "membackend/simpleMemBackend.h"
#include "membackend/simpleMemBackendConvertor.h"

using namespace SST;
using namespace SST::Interfaces;
using namespace SST::MemHierarchy;

/*------------------------------- Simple Backend ------------------------------- */
SimpleMemory::SimpleMemory(ComponentId_t id, Params &params) : SimpleMemBackend(id, params){ 
    std::string access_time = params.find<std::string>("access_time", "100 ns");
    self_link = configureSelfLink("Self", access_time,
            new Event::Handler<SimpleMemory>(this, &SimpleMemory::handleSelfEvent));

    m_maxReqPerCycle = params.find<>("max_requests_per_cycle", 1);
}

void SimpleMemory::handleSelfEvent(SST::Event *event){

    //测试event类型
    // SST::Event *event1 = event;
    // SST::Event *event2 = event;
    // SST::Event *event3 = event;
    // SST::Interfaces::StandardMem::Read *read = dynamic_cast<SST::Interfaces::StandardMem::Read*>(event1);
    // SST::Interfaces::StandardMem::Write *write = dynamic_cast<SST::Interfaces::StandardMem::Write*>(event2);
    // MemEvent *mev = dynamic_cast<MemEvent*>(event3);
    // if(read != NULL){
    //     std::cout << "read addr: " << std::hex << read->pAddr << std::endl;
    // }else if(write != NULL){
    //     std::cout << "write addr: " << std::hex << write->pAddr << std::endl;
    // }else if(mev != NULL){
    //     std::cout << "mev addr: " << std::hex << mev->getAddr() << std::endl;
    // }else{
    //     std::cout << "Not read!" << std::endl;
    // }
    MemCtrlEvent *ev = static_cast<MemCtrlEvent*>(event);
#ifdef __SST_DEBUG_OUTPUT__
    output->debug(_L10_, "%s: Transaction done for id %" PRIx64 "\n", getName().c_str(),ev->reqId);
#endif
    handleMemResponse(ev->reqId);

    // 测试函数调用
    // std::cout << "Hello, World! Again！" << std::endl;
    delete event;
}

bool SimpleMemory::issueRequest(ReqId id, Addr addr, bool isWrite, unsigned numBytes ){
#ifdef __SST_DEBUG_OUTPUT__
    output->debug(_L10_, "%s: Issued transaction for address %" PRIx64 " id %" PRIx64"\n", getName().c_str(),(Addr)addr,id);
#endif
    self_link->send(1, new MemCtrlEvent(id));
    return true;
}

